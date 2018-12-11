## Wikipedia IDF
> Wikipedia document terms frequency.

### 1. downalod wiki dump
eg:
```
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

or
wget https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2
```

### 2. extractor
Process it with: [wikiextractor][https://github.com/attardi/wikiextractor]
```
python WikiExtractor.py -o ./extract_dir --compress --json /path/to/enwiki-latest-pages-articles.xml.bz2

or
[中文维基百科数据处理][https://bamtercelboo.github.io/2018/05/10/wikidata_Process/]
```


### 3. IDF
```
python wikipediaidf.py -i ./extract_dir -o ./idf_save_path -s english -c 4
```

### 4. result
csf format
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


