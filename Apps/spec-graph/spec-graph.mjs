#!/usr/bin/env node

/**
 * spec-graph CLI — Thin wrapper over spec-graph-lib.
 *
 * Commands:
 *   build              Generate _build/graph.json (+ optional --html)
 *   visualize          Generate _build/graph.mermaid
 *   impact <spec-id>   Show specs affected by a change (transitive BFS)
 *   orphans            List specs with no inbound or outbound edges
 *   validate           Check integrity (broken IDs, cycles, confidence)
 *   stats              Show metrics (specs per layer, domain, coverage)
 *   filter             Filter specs by composable criteria
 *   path <from> <to>   Find shortest path between two specs
 *   context <spec-id>  Contextual activation bundle for a spec
 */

import { program } from 'commander';
import { writeFileSync, mkdirSync, readFileSync } from 'fs';
import { join, resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

import {
  buildGraph,
  impactBFS,
  findOrphans,
  validateGraph,
  generateMermaid,
  filterSpecs,
  findPath,
  buildContext,
  buildActivationContext,
  LAYER_COLORS,
} from './spec-graph-lib.mjs';

// ─── CLI Helpers ──────────────────────────────────────────────────────────────

const BUILD_DIR = '_build';
const __dirname = dirname(fileURLToPath(import.meta.url));

function ensureBuildDir() {
  mkdirSync(BUILD_DIR, { recursive: true });
}

function resolveSpecsDir(opts) {
  return resolve(opts.specs || '.');
}

function getGraph(opts) {
  return buildGraph(resolveSpecsDir(opts));
}

// ─── Program Setup ────────────────────────────────────────────────────────────

program
  .name('spec-graph')
  .description('Derive a knowledge graph from spec YAML frontmatters')
  .version('0.2.0')
  .option('-s, --specs <dir>', 'Directory containing specs (scans recursively)', '.');

// ── build ─────────────────────────────────────────────────────────────────────

program
  .command('build')
  .description('Generate _build/graph.json (add --html for interactive viewer)')
  .option('--html', 'Also generate _build/graph.html interactive viewer')
  .action((cmdOpts, cmd) => {
    const opts = cmd.optsWithGlobals();
    const graph = getGraph(opts);

    ensureBuildDir();
    const outPath = join(BUILD_DIR, 'graph.json');
    writeFileSync(outPath, JSON.stringify(graph, null, 2));

    console.log(`Graph built: ${graph.metadata.spec_count} specs, ${graph.metadata.edge_count} edges`);
    console.log(`Output: ${outPath}`);

    if (cmdOpts.html) {
      try {
        const viewerTemplate = readFileSync(join(__dirname, 'spec-graph-viewer.html'), 'utf-8');
        const htmlContent = viewerTemplate.replace(
          '"__GRAPH_DATA__"',
          JSON.stringify(graph)
        );
        const htmlPath = join(BUILD_DIR, 'graph.html');
        writeFileSync(htmlPath, htmlContent);
        console.log(`Viewer: ${htmlPath}`);
      } catch (err) {
        console.error(`Could not generate HTML viewer: ${err.message}`);
      }
    }

    if (graph._errors.length > 0) {
      console.log(`\nWarnings (${graph._errors.length}):`);
      for (const err of graph._errors) {
        console.log(`  - ${err.file}: ${err.error}`);
      }
    }
  });

// ── visualize ─────────────────────────────────────────────────────────────────

program
  .command('visualize')
  .description('Generate _build/graph.mermaid diagram')
  .action((_, cmd) => {
    const opts = cmd.optsWithGlobals();
    const graph = getGraph(opts);
    const mermaid = generateMermaid(graph);

    ensureBuildDir();
    const outPath = join(BUILD_DIR, 'graph.mermaid');
    writeFileSync(outPath, mermaid);

    console.log(`Mermaid diagram generated: ${graph.metadata.spec_count} specs`);
    console.log(`Output: ${outPath}`);
    console.log('\n' + mermaid);
  });

// ── impact ────────────────────────────────────────────────────────────────────

program
  .command('impact <spec-id>')
  .description('Show specs transitively affected by a change to <spec-id>')
  .action((specId, _, cmd) => {
    const opts = cmd.optsWithGlobals();
    const graph = getGraph(opts);
    const nodeIds = new Set(graph.nodes.map((n) => n.id));

    if (!nodeIds.has(specId)) {
      console.error(`Error: Spec "${specId}" not found in the graph.`);
      console.error(`Known specs: ${[...nodeIds].join(', ')}`);
      process.exit(1);
    }

    const affected = impactBFS(specId, graph.edges, graph.nodes);

    if (affected.length === 0) {
      console.log(`No specs are affected by changes to "${specId}".`);
      return;
    }

    console.log(`Impact analysis for "${specId}":\n`);
    console.log(`${affected.length} spec(s) affected:\n`);

    for (const item of affected) {
      const node = item.node;
      const status = node ? `[${node.status}/${node.confidence}]` : '[unknown]';
      console.log(`  ${item.id} ${status}`);
      console.log(`    Relation: ${item.relation} (via ${item.via})`);
      if (node) console.log(`    File: ${node.file}`);
      console.log('');
    }
  });

// ── orphans ───────────────────────────────────────────────────────────────────

program
  .command('orphans')
  .description('List specs with no inbound or outbound dependencies')
  .action((_, cmd) => {
    const opts = cmd.optsWithGlobals();
    const graph = getGraph(opts);
    const orphans = findOrphans(graph.nodes, graph.edges);

    if (orphans.length === 0) {
      console.log('No orphan specs found. All specs are connected.');
      return;
    }

    console.log(`${orphans.length} orphan spec(s) found:\n`);
    for (const id of orphans) {
      const node = graph.nodes.find((n) => n.id === id);
      console.log(`  ${id} [${node.status}/${node.confidence}]`);
      console.log(`    File: ${node.file}`);
    }
  });

// ── validate ──────────────────────────────────────────────────────────────────

program
  .command('validate')
  .description('Check integrity: broken refs, duplicate IDs, cycles, deprecated refs')
  .action((_, cmd) => {
    const opts = cmd.optsWithGlobals();
    const graph = getGraph(opts);
    const issues = validateGraph(graph);

    if (graph._errors.length > 0) {
      console.log(`Parse errors (${graph._errors.length}):`);
      for (const err of graph._errors) {
        console.log(`  ERROR  ${err.file}: ${err.error}`);
      }
      console.log('');
    }

    if (issues.length === 0 && graph._errors.length === 0) {
      console.log('Validation passed. No issues found.');
      console.log(`Checked ${graph.metadata.spec_count} specs, ${graph.metadata.edge_count} edges.`);
      process.exit(0);
      return;
    }

    const errors = issues.filter((i) => i.severity === 'error');
    const warnings = issues.filter((i) => i.severity === 'warning');

    if (errors.length > 0) {
      console.log(`Errors (${errors.length}):`);
      for (const issue of errors) {
        console.log(`  ERROR  [${issue.type}] ${issue.message}`);
      }
      console.log('');
    }

    if (warnings.length > 0) {
      console.log(`Warnings (${warnings.length}):`);
      for (const issue of warnings) {
        console.log(`  WARN   [${issue.type}] ${issue.message}`);
      }
      console.log('');
    }

    console.log(`Summary: ${errors.length} error(s), ${warnings.length} warning(s)`);

    if (errors.length > 0) {
      process.exit(1);
    }
  });

// ── stats ─────────────────────────────────────────────────────────────────────

program
  .command('stats')
  .description('Show metrics: specs per layer, domain, confidence distribution')
  .action((_, cmd) => {
    const opts = cmd.optsWithGlobals();
    const graph = getGraph(opts);
    const orphans = findOrphans(graph.nodes, graph.edges);

    console.log('=== KDD Knowledge Graph — Statistics ===\n');
    console.log(`Total specs:  ${graph.metadata.spec_count}`);
    console.log(`Total edges:  ${graph.metadata.edge_count}`);
    console.log(`Orphans:      ${orphans.length}`);

    const groupBy = (arr, key) => {
      const map = {};
      for (const item of arr) {
        const val = item[key] || 'unspecified';
        map[val] = (map[val] || 0) + 1;
      }
      return Object.entries(map).sort((a, b) => b[1] - a[1]);
    };

    console.log('\nBy axis:');
    for (const [val, count] of groupBy(graph.nodes, '_axis')) {
      const scope = val === 'knowledge' ? '(persistent)' : val === 'work' ? '(ephemeral)' : val === 'governance' ? '(bridge)' : '';
      console.log(`  ${val}: ${count} ${scope}`);
    }

    console.log('\nBy layer:');
    for (const [val, count] of groupBy(graph.nodes, 'layer')) console.log(`  ${val}: ${count}`);

    console.log('\nBy domain:');
    for (const [val, count] of groupBy(graph.nodes, 'domain')) console.log(`  ${val}: ${count}`);

    console.log('\nBy status:');
    for (const [val, count] of groupBy(graph.nodes, 'status')) console.log(`  ${val}: ${count}`);

    console.log('\nBy confidence:');
    for (const [val, count] of groupBy(graph.nodes, 'confidence')) console.log(`  ${val}: ${count}`);

    const avgDeps = graph.metadata.edge_count / Math.max(graph.metadata.spec_count, 1);
    console.log(`\nAvg dependencies per spec: ${avgDeps.toFixed(1)}`);

    if (graph.edges.length > 0) {
      console.log('\nBy relation type:');
      const byRel = {};
      for (const edge of graph.edges) {
        byRel[edge.relation] = (byRel[edge.relation] || 0) + 1;
      }
      for (const [rel, count] of Object.entries(byRel).sort((a, b) => b[1] - a[1])) {
        console.log(`  ${rel}: ${count}`);
      }
    }
  });

// ── filter (Phase 2) ─────────────────────────────────────────────────────────

program
  .command('filter')
  .description('Filter specs by composable criteria (AND logic)')
  .option('--layer <layer>', 'Filter by layer')
  .option('--domain <domain>', 'Filter by domain')
  .option('--subdomain <subdomain>', 'Filter by subdomain')
  .option('--confidence <level>', 'Filter by confidence (high/medium/low)')
  .option('--status <status>', 'Filter by status (draft/active/deprecated)')
  .option('--tag <tag>', 'Filter by tag')
  .option('--type <type>', 'Filter by spec type')
  .option('--axis <axis>', 'Filter by axis (knowledge/work/governance)')
  .option('--scope <scope>', 'Filter by scope (persistent/ephemeral)')
  .option('--format <fmt>', 'Output format: table (default) or json', 'table')
  .action((cmdOpts, cmd) => {
    const opts = cmd.optsWithGlobals();
    const graph = getGraph(opts);

    const criteria = {};
    for (const key of ['layer', 'domain', 'subdomain', 'confidence', 'status', 'tag', 'type', 'axis', 'scope']) {
      if (cmdOpts[key]) criteria[key] = cmdOpts[key];
    }

    const results = filterSpecs(graph, criteria);

    if (cmdOpts.format === 'json') {
      console.log(JSON.stringify(results, null, 2));
      return;
    }

    if (results.length === 0) {
      console.log('No specs match the given criteria.');
      return;
    }

    console.log(`${results.length} spec(s) found:\n`);
    for (const node of results) {
      console.log(`  ${node.id} [${node.layer}] [${node.status}/${node.confidence}]`);
      if (node.title) console.log(`    ${node.title}`);
      console.log(`    Domain: ${node.domain || '-'}  File: ${node.file}`);
      console.log('');
    }
  });

// ── path (Phase 2) ───────────────────────────────────────────────────────────

program
  .command('path <from> <to>')
  .description('Find shortest path between two specs')
  .action((from, to, _, cmd) => {
    const opts = cmd.optsWithGlobals();
    const graph = getGraph(opts);
    const nodeIds = new Set(graph.nodes.map((n) => n.id));

    for (const id of [from, to]) {
      if (!nodeIds.has(id)) {
        console.error(`Error: Spec "${id}" not found. Known specs: ${[...nodeIds].join(', ')}`);
        process.exit(1);
      }
    }

    const path = findPath(from, to, graph.edges, graph.nodes);

    if (!path) {
      console.log(`No path found between "${from}" and "${to}".`);
      return;
    }

    console.log(`Path from "${from}" to "${to}" (${path.length - 1} hop(s)):\n`);

    for (let i = 0; i < path.length; i++) {
      const step = path[i];
      const node = graph.nodes.find((n) => n.id === step.id);
      const label = node ? `[${node.layer}]` : '';

      if (i === 0) {
        console.log(`  ${step.id} ${label}`);
      } else {
        const arrow = step.direction === 'outgoing' ? '──>' : '<──';
        console.log(`    ${arrow} ${step.relation}`);
        console.log(`  ${step.id} ${label}`);
      }
    }
  });

// ── context (Phase 2) ────────────────────────────────────────────────────────

program
  .command('context <spec-id>')
  .description('Contextual activation: get spec + neighborhood bundle (tiered for work artifacts)')
  .option('-d, --depth <n>', 'Traversal depth', '3')
  .option('--format <fmt>', 'Output format: markdown (default) or json', 'markdown')
  .action((specId, cmdOpts, cmd) => {
    const opts = cmd.optsWithGlobals();
    const graph = getGraph(opts);
    const depth = parseInt(cmdOpts.depth, 10) || 3;

    const rootNode = graph.nodes.find((n) => n.id === specId);
    if (!rootNode) {
      console.error(`Error: Spec "${specId}" not found.`);
      const nodeIds = graph.nodes.map((n) => n.id);
      console.error(`Known specs: ${nodeIds.join(', ')}`);
      process.exit(1);
    }

    // Use tiered activation context for work artifacts, classic for others
    const isWork = rootNode._axis === 'work';

    if (isWork) {
      const ctx = buildActivationContext(specId, graph, { depth });

      if (cmdOpts.format === 'json') {
        console.log(JSON.stringify(ctx, null, 2));
        return;
      }

      console.log(`# Activation Context: ${specId}\n`);
      console.log(`Depth: ${depth} | Total specs: ${ctx.totalSpecs} | Explicitly activated: ${ctx.activatedCount}\n`);

      const TIER_LABELS = {
        1: 'Full Context',
        2: 'Summary',
        3: 'Reference Only',
      };

      for (const tier of [1, 2, 3]) {
        const specs = ctx.byTier[tier];
        if (specs.length === 0) continue;

        console.log(`## Tier ${tier} — ${TIER_LABELS[tier]} (${specs.length})\n`);

        for (const spec of specs) {
          const explicit = spec._explicit ? ' (declared)' : ` (transitive via ${spec._via})`;
          if (tier <= 2) {
            console.log(`### ${spec.id}${explicit}`);
            if (spec.title) console.log(`**${spec.title}**`);
            console.log(`- Layer: ${spec.layer} | Status: ${spec.status} | Confidence: ${spec.confidence}`);
            console.log(`- Domain: ${spec.domain || '-'} > ${spec.subdomain || '-'}`);
            console.log(`- File: ${spec.file}`);
            console.log('');
          } else {
            console.log(`- ${spec.id} [${spec.layer}] — ${spec.title || 'Untitled'}`);
          }
        }
        console.log('');
      }
    } else {
      // Classic context for non-work specs
      const ctx = buildContext(specId, graph, { depth });

      if (cmdOpts.format === 'json') {
        console.log(JSON.stringify(ctx, null, 2));
        return;
      }

      console.log(`# Context: ${specId}\n`);
      console.log(`Depth: ${depth} | Total specs in context: ${ctx.totalSpecs}\n`);

      for (const [layer, specs] of Object.entries(ctx.byLayer)) {
        console.log(`## ${layer} (${specs.length})\n`);
        for (const spec of specs) {
          const depthLabel = spec._contextDepth === 0 ? ' (root)' : ` (depth ${spec._contextDepth})`;
          console.log(`### ${spec.id}${depthLabel}`);
          if (spec.title) console.log(`**${spec.title}**`);
          console.log(`- Status: ${spec.status} | Confidence: ${spec.confidence}`);
          console.log(`- Domain: ${spec.domain || '-'} > ${spec.subdomain || '-'}`);
          console.log(`- File: ${spec.file}`);
          if (spec.tags && spec.tags.length > 0) {
            console.log(`- Tags: ${spec.tags.join(', ')}`);
          }
          if (spec._contextRelations.length > 0) {
            for (const rel of spec._contextRelations) {
              console.log(`- Reached via: ${rel.relation} from ${rel.from} (${rel.direction})`);
            }
          }
          console.log('');
        }
      }
    }
  });

program.parse();
