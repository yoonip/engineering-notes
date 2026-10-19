'use strict';
const path = require('path');
const fs = require('fs');
const CONFIG_NAMES = new Set([
    'Python 현재 파일 (input.txt 자동 입력)', 'C++ 현재 파일 (input.txt 자동 입력)', 'C 현재 파일 (input.txt 자동 입력)',
    'Python 현재 파일 (키보드 입력)', 'C++ 현재 파일 (키보드 입력)', 'C 현재 파일 (키보드 입력)'
]);

function normalizePath(value) {
    return path.win32.resolve(value).replace(/[\\/]+$/, '').toLowerCase();
}
function isPracticeFolder(folder) {
    return !!folder && folder.uri && folder.uri.scheme === 'file' &&
        fs.existsSync(path.join(folder.uri.fsPath, 'scripts', 'run.ps1')) &&
        fs.existsSync(path.join(folder.uri.fsPath, 'samples'));
}
function languageOf(source) {
    switch (path.win32.extname(source).toLowerCase()) {
        case '.py': return 'Python';
        case '.cpp': case '.cc': case '.cxx': return 'C++';
        case '.c': return 'C';
        default: return undefined;
    }
}
function isInsidePractice(source, folder) {
    if (!isPracticeFolder(folder)) return false;
    const relative = path.win32.relative(folder.uri.fsPath, source);
    return relative !== '' && !path.win32.isAbsolute(relative) && relative !== '..' && !relative.startsWith('..\\');
}
function launchName(language, keyboard = false) {
    return `${language} 현재 파일 (${keyboard ? '키보드 입력' : 'input.txt 자동 입력'})`;
}
function routeConfiguration(folder, configuration, source, configurations) {
    if (!isPracticeFolder(folder) || !CONFIG_NAMES.has(configuration.name) || configuration.request !== 'launch'
        || !['debugpy', 'cppdbg'].includes(configuration.type) || !source || !isInsidePractice(source, folder)) {
        return configuration;
    }
    const language = languageOf(source);
    if (!language) return configuration;
    const name = launchName(language, configuration.name.includes('(키보드 입력)'));
    const type = language === 'Python' ? 'debugpy' : 'cppdbg';
    // Keep all attributes already resolved by another provider when no switch is needed.
    if (configuration.name === name && configuration.type === type) return configuration;
    const target = configurations.find(item => item.name === name && item.type === type && item.request === 'launch');
    if (!target) return configuration;
    const resolved = JSON.parse(JSON.stringify(target));
    if (Object.prototype.hasOwnProperty.call(configuration, 'noDebug')) resolved.noDebug = configuration.noDebug;
    if (Object.prototype.hasOwnProperty.call(configuration, '__configurationTarget')) resolved.__configurationTarget = configuration.__configurationTarget;
    return resolved;
}
module.exports = { CONFIG_NAMES, isPracticeFolder, languageOf, isInsidePractice, launchName, routeConfiguration };
