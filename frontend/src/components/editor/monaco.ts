// Bundle the editor and worker locally: no CDN request or eval permission needed.
import { loader } from '@monaco-editor/react';
import * as monaco from 'monaco-editor/editor/editor.api';
import 'monaco-editor/languages/definitions/python/register.js';
import EditorWorker from 'monaco-editor/editor/editor.worker?worker';

self.MonacoEnvironment = { getWorker: () => new EditorWorker() };
loader.config({ monaco });
// Expose the same editor API used by the browser exercise regression tests.
Object.assign(window, { monaco });
