#!/usr/bin/env node
import { mkdirSync, cpSync, rmSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const home = homedir();
const dest = join(home, '.claude', 'skills', 'accounting-skills');

// Clean previous install
if (existsSync(dest)) {
  rmSync(dest, { recursive: true });
}
mkdirSync(dest, { recursive: true });

// Copy skill files
const dirs = ['references', 'templates', 'scripts'];
cpSync(join(__dirname, 'SKILL.md'), join(dest, 'SKILL.md'));
cpSync(join(__dirname, 'LICENSE.txt'), join(dest, 'LICENSE.txt'));

for (const dir of dirs) {
  const src = join(__dirname, dir);
  if (existsSync(src)) {
    cpSync(src, join(dest, dir), { recursive: true });
  }
}

console.log();
console.log('  ✓ Installed @cynco/accounting-skills');
console.log(`  → ${dest}/`);
console.log();
console.log('  Next steps:');
console.log('  1. Replace placeholders in the skill files:');
console.log(`     grep -r "[PRACTICE_NAME]" "${dest}"`);
console.log('  2. Point Claude at a client folder and say:');
console.log('     "process the accounts for this client"');
console.log();
