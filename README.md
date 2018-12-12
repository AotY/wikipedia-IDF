## Wikipedia IDF
> Wikipedia document terms frequency.

### 1. downalod wiki dump
eg:
```
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2 -P ./data

or
wget https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2 -P ./data
```

### 2. extractor
Process it with: [wikiextractor][https://github.com/attardi/wikiextractor]
```
python wiki_extractor.py -o ./data/en_extract_dir --compress --json ./data/enwiki-latest-pages-articles.xml.bz2

or

python wiki_extractor.py -o ./data/zh_extract_dir --compress --json ./data/zhwiki-latest-pages-articles.xml.bz2

参考： [中文维基百科数据处理][https://bamtercelboo.github.io/2018/05/10/wikidata_Process/]
```


### 3. IDF
```
python wiki_idf.py -i ./data/en_extract_dir -o ./data/idf_save_path/en -lang english -s -c 6

or

python wiki_idf.py -i ./data/zh_extract_dir -o ./data/idf_save_path/zh -lang chinese -c 6
```

### 4. result
csv format
```
token,frequency,total,idf
the,4868104,5375019,0.09905756998426586
in,4677480,5375019,0.13900260552258173
a,4634606,5375019,0.14821091888028787
...
```

if language has stem, eg:
```
stem,frequency,total,idf,most_freq_term
sinc,756750,5375019,1.9604831185320117,since
sever,756035,5375019,1.9614283937799355,several
call,754768,5375019,1.9631056457046039,called
than,736545,5375019,1.9875456963514588,than
[...]

```


