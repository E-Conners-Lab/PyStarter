import Editor from '@monaco-editor/react';

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  height?: string;
  readOnly?: boolean;
}

export default function CodeEditor({
  value,
  onChange,
  height = '300px',
  readOnly = false,
}: CodeEditorProps) {
  return (
    <Editor
      height={height}
      defaultLanguage="python"
      value={value}
      onChange={(val) => onChange(val || '')}
      theme="vs-dark"
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        lineNumbers: 'on',
        scrollBeyondLastLine: false,
        automaticLayout: true,
        tabSize: 4,
        insertSpaces: true,
        wordWrap: 'on',
        readOnly,
        renderLineHighlight: 'line',
        padding: { top: 12, bottom: 12 },
        suggestOnTriggerCharacters: true,
        quickSuggestions: true,
      }}
    />
  );
}
