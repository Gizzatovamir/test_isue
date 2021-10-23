# test_isue
Test task

## Tweeter scraper
```bash
twitter_scraper.py 
```
Creates 3 .csv files, that contains:
- Chosen celebrity tweets
- Celebrity replies with filter "-from:<Celbrity username> -filter:replies"
- All tweets about what celebrity said, celebrity once said and celebrity mentioning

All files are filtered from emijis, links and other symbols.
However are no NLP filtering(because there are no pretrained models in internet )
P.s. All repos with weights\models had trash readme, so there werent a chance to run them

### eval
to recrate all .csv files you need to run:
  ```bash
  python3 twitter_scraper.py 
  ```
with changing parametrs to your notice 
  
## Youtube subtitles
  
```bash
  get_subtitles.py
```
- Creates a json with template:
  ```json
  [
    "<Celebrity name>":
      [
        "question_<question number>": "<qusetion>",
        "answer_<answer number>": "<answer>"
      ],
  
  ]
  ```
### eval
to recrate same .json files you need to run:
  ```bash
  python3 get_subtitles.py
  ```

Tried to get timings of celebrity and interviwer speaking, but failed to run voxceleb trained models. So decieded to make correspondence between even and uneven texts in an array.
