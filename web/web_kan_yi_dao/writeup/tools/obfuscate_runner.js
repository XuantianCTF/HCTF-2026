// kan-yi-dao 前端混淆 runner（出题方工具，构建期运行，需要 node>=18）
// 用法: node obfuscate_runner.js <in.js> <out.js>
// 约束:
//  - reservedStrings 豁免 16+ 位的 base64 形态字面量（TRACK.tok/ts 必须留原位，
//    exp.py 靠 `tok: '...'` 正则提取验收；_tk() 运行时解码不受影响）
//  - 不开 controlFlowFlattening / deadCodeInjection / debugProtection:
//    页面动画密集，保性能；debugProtection 属敌意反调试，不适合比赛题
//  - 零宽 __bp 不进混淆（字符串数组化会毁灭字面 U+200B/U+200C），
//    由 build_frontend.py 在混淆产物之前以独立语句注入
const fs = require('fs');
const JavaScriptObfuscator = require('javascript-obfuscator');

const [infile, outfile] = process.argv.slice(2);
if (!infile || !outfile) {
  console.error('usage: node obfuscate_runner.js <in.js> <out.js>');
  process.exit(2);
}

const src = fs.readFileSync(infile, 'utf8');
const result = JavaScriptObfuscator.obfuscate(src, {
  compact: true,
  simplify: false,
  identifierNamesGenerator: 'hexadecimal',
  renameGlobals: false,
  selfDefending: false,
  controlFlowFlattening: false,
  deadCodeInjection: false,
  debugProtection: false,
  disableConsoleOutput: false,
  stringArray: true,
  stringArrayEncoding: ['base64'],
  stringArrayRotate: true,
  stringArrayShuffle: true,
  stringArrayThreshold: 1,
  stringArrayWrappersCount: 1,
  stringArrayWrappersType: 'variable',
  splitStrings: false,
  unicodeEscapeSequence: false,
  transformObjectKeys: false,
  reservedStrings: ['^[A-Za-z0-9+/=]{16,}$'],
});

fs.writeFileSync(outfile, result.getObfuscatedCode(), 'utf8');
console.error('obfuscated %d -> %d bytes', src.length, result.getObfuscatedCode().length);
