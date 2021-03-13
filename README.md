# twitter-to-hatena

Post tweets to hatena blog with photos, tags.

## Demo

You can post your tweets to Hatena blog in a single article for each day.  
The sample of tweet and posted article (archives view).

**Tweets**

<img width="599" alt="twitter" src="https://user-images.githubusercontent.com/16054638/111025345-ddd0bb80-8426-11eb-91c1-74c19506fb45.png">

**Posted articles**

<img width="962" alt="blog" src="https://user-images.githubusercontent.com/16054638/111025351-e9bc7d80-8426-11eb-90d1-7a3c9bd93236.png">

## Description

* A day's worth of tweets will be compiled into a single article.
* The hashtag of the tweet is exported as a category.
* Only photo media can be exported to blog.
* The title of blog entry will be "YYYY-MM-DD".
* You have to apply [twitter developer](https://developer.twitter.com/en) with your twitter account, and get your access tokens.

## Precautions

* If you fork this repository and use your github actions, please check the [github's terms of service](https://docs.github.com/en/github/site-policy/github-additional-product-terms#5-actions-and-packages)

## Usage

**Required environment**

* python >= 3.7

**Preparation**

* Apply Twitter Developer account and get customer key & access token for OAuth
* Create Hatena accuont and get hatena api-key

### from local

**daily export**

```
$ git clone git@github.com:kusuwada/twitter-to-hatena.git
$ cd twitter-to-hatena
$ pip install -r requirements.txt
$ export TW_CK={twitter_customer_key}
$ export TW_CKS={twitter_customer_key_secret}
$ export TW_AT={twitter_access_token}
$ export TW_ATS={twitter_access_token_secret}
$ export HT_KEY={hatena_api_key}
$ python daily.py {YYYY-MM-DD} {twitter_username} {hatena_id} {hatena_root_endpoint} {tmp_path} --tz={timezone(Default: 'Etc/UTC')}
```

**batch export**

```
$ git clone git@github.com:kusuwada/twitter-to-hatena.git
$ cd twitter-to-hatena
$ pip install -r requirements.txt
$ export TW_CK={twitter_customer_key}
$ export TW_CKS={twitter_customer_key_secret}
$ export TW_AT={twitter_access_token}
$ export TW_ATS={twitter_access_token_secret}
$ export HT_KEY={hatena_api_key}
$ python batch.py {YYYY-MM-DD} {YYYY-MM-DD} {twitter_username} {hatena_id} {hatena_root_endpoint} {tmp_path} --tz={timezone(Default: 'Etc/UTC')}
```

### from act

* Install [nektos/act](https://github.com/nektos/act) and setup to your machine.

**daily export**

```
$ act -j daily -s TW_CK={twitter_customer_key} -s TW_CKS={twitter_customer_key_secret} -s TW_AT={twitter_access_token} -s TW_ATS={twitter_access_token_secret} -s HT_KEY={hatena_api_key} -P ubuntu-latest=nektos/act-environments-ubuntu:18.04
```

**batch export**

* Create `./test/test.event` file

```json
{
  "action": "workflow_dispatch",
  "inputs": {
      "start": "2021-03-01",
      "end": "2021-03-10"
  }
}
```

*Chenage start & end date as you like

```
act workflow_dispatch --eventpath test/test.event -s TW_CK={twitter_customer_key} -s TW_CKS={twitter_customer_key_secret} -s TW_AT={twitter_access_token} -s TW_ATS={twitter_access_token_secret} -s HT_KEY={hatena_api_key} -P ubuntu-latest=nektos/act-environments-ubuntu:18.04
```

### The setting of Hatena blog

* Recommended edit mode: Markdown mode

## Limitation

* Movie or GIF is not exported.
* The limitation of posting entry number to Hatena Blog is 100 / 24h.