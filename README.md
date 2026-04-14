# listener-letter-generator
ラジオのリスナーからのお便りをAIで生成します

## 実行方法
```bash
uv run .\main.py -n=10
```

### テーマを指定する場合
```bash
uv run .\main.py -n=5 --theme "怪談" --description "怖い話、不思議な話、意味がわかると怖い話などを送ってください"
```
省略時はフリーテーマになります。
