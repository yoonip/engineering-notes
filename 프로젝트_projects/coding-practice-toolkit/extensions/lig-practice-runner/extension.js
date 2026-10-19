'use strict';
const vscode = require('vscode');
const router = require('./router');

function activate(context) {
    const output = vscode.window.createOutputChannel('Practice 자동 실행');
    context.subscriptions.push(output);
    function editorSource() {
        const editor = vscode.window.activeTextEditor;
        return editor && editor.document.uri.scheme === 'file' ? editor.document.uri.fsPath : undefined;
    }
    function updateContext() {
        const editor = vscode.window.activeTextEditor;
        const source = editorSource();
        const folder = editor ? vscode.workspace.getWorkspaceFolder(editor.document.uri) : undefined;
        const enabled = router.isPracticeFolder(folder) && !!source && router.isInsidePractice(source, folder);
        return vscode.commands.executeCommand('setContext', 'ligPractice.workspace', enabled);
    }
    void updateContext();
    context.subscriptions.push(vscode.workspace.onDidChangeWorkspaceFolders(updateContext));
    context.subscriptions.push(vscode.window.onDidChangeActiveTextEditor(updateContext));

    async function runTask(folder, source, keyboard) {
        const name = keyboard ? '현재 파일 실행 (키보드 입력)' : '현재 파일 실행 (input.txt 자동 입력)';
        // TaskFilter.type is a definition type, not ProcessExecution versus ShellExecution.
        // Configured process tasks can therefore be omitted by a "process" filter.
        const tasks = await vscode.tasks.fetchTasks();
        output.appendLine('작업 목록: ' + tasks.map(item => `${item.name} [${item.scope && item.scope.uri ? item.scope.uri.fsPath : String(item.scope)}]`).join(', '));
        const task = tasks.find(item => item.name === name &&
            (router.isPracticeFolder(item.scope) ||
                ((typeof item.scope === 'number' || item.scope === undefined) && (vscode.workspace.workspaceFolders || []).length === 1 &&
                    router.isPracticeFolder(vscode.workspace.workspaceFolders[0]))));
        if (!task) {
            await vscode.window.showErrorMessage(`실행 작업 '${name}'을 찾지 못했습니다. 현재 연습 프로젝트 폴더를 다시 열어 주세요.`);
            return false;
        }
        output.appendLine(`실행: ${source} → ${name}`);
        await vscode.tasks.executeTask(task);
        return true;
    }

    async function runCurrent(noDebug) {
        const editor = vscode.window.activeTextEditor;
        const source = editorSource();
        const folder = editor ? vscode.workspace.getWorkspaceFolder(editor.document.uri) : undefined;
        const language = source && router.languageOf(source);
        if (!router.isPracticeFolder(folder) || !source || !router.isInsidePractice(source, folder) || !language) {
            await vscode.window.showInformationMessage('현재 연습 프로젝트 안의 .py / .cpp / .c 코드 탭을 선택한 뒤 실행하세요.');
            return false;
        }
        if (!(await editor.document.save())) return false;
        if (noDebug) return runTask(folder, source, false);
        const name = router.launchName(language);
        output.appendLine(`${noDebug ? '실행' : '디버깅'}: ${source} → ${name}`);
        return vscode.debug.startDebugging(folder, name, { noDebug });
    }
    context.subscriptions.push(vscode.commands.registerCommand('ligPractice.debugCurrent', () => runCurrent(false)));
    context.subscriptions.push(vscode.commands.registerCommand('ligPractice.runCurrent', () => runCurrent(true)));

    const provider = {
        async resolveDebugConfiguration(folder, configuration) {
            if (!router.isPracticeFolder(folder) || !router.CONFIG_NAMES.has(configuration.name)) return configuration;
            const source = editorSource();
            if (!source || !router.isInsidePractice(source, folder) || !router.languageOf(source)) {
                await vscode.window.showInformationMessage('실행할 .py / .cpp / .c 코드 탭을 선택한 뒤 다시 실행하세요.');
                return undefined;
            }
            if (configuration.noDebug === true) {
                await runTask(folder, source, configuration.name.includes('(키보드 입력)'));
                // Abort debugger creation; the existing run task owns this execution.
                // undefined cancels quietly, whereas null would open launch.json.
                return undefined;
            }
            const configurations = vscode.workspace.getConfiguration('launch', folder.uri).get('configurations', []);
            const routed = router.routeConfiguration(folder, configuration, source, configurations);
            if (routed !== configuration) output.appendLine(`설정 자동 선택: ${configuration.name} → ${routed.name}`);
            return routed;
        }
    };
    // The initial hook runs before variable substitution, preLaunchTask and adapter creation.
    // VS Code repeats initial resolution for a changed debug type, so both directions work.
    context.subscriptions.push(vscode.debug.registerDebugConfigurationProvider('debugpy', provider));
    context.subscriptions.push(vscode.debug.registerDebugConfigurationProvider('cppdbg', provider));
}
function deactivate() {}
module.exports = { activate, deactivate };
