# Acknowlege
This is a Forked Repository from Zhengyao Jiang and his colleage's work(https://github.com/ZhengyaoJiang/PGPortfolio), which is the original implementation of our paper, A Deep Reinforcement Learning Framework for the Financial Portfolio Management Problem (arXiv:1706.10059)
## Platform Support
Python 3.5+ in windows and Python 2.7+/3.5+ in linux are supported.

## Dependencies
Install Dependencies via `pip install -r requirements.txt`

* tensorflow (>= 1.0.0)
* tflearn
* pandas
* ...

# User Guide
## Configuration File
Under the `nntrader/nntrader` directory, there is a json file called `net_config.json`,
 holding all the configuration of the agent and could be modified outside the program code.
### Network Topology
* `"layers"`
    * layers list of the CNN, including the output layer
    * `"type"`
        * domain is {"ConvLayer", "FullyLayer", "DropOut", "MaxPooling",
        "AveragePooling", "LocalResponseNormalization", "SingleMachineOutput",
        "LSTMSingleMachine", "RNNSingleMachine"}
    * `"filter shape"`
        * shape of the filter (kernal) of the Convolution Layer
* `"input"`
    * `"window_size"`
        * number of columns of the input matrix
    * `"coin_number"`
        * number of rows of the input matrix
    * `"feature_number"`
        * number of features (just like RGB in computer vision)
        * domain is {1, 2, 3}
        * 1 means the feature is ["close"], last price of each period
        * 2 means the feature is ["close", "volume"]
        * 3 means the features are ["close", "high", "low"]

### Market Data
* `"input "`
    * `"start_date"`
        * start date of the global data matrix
        * format is yyyy/MM/dd
    * `"end_date"`
        * start date of the global data matrix
        * format is yyyy/MM/dd
        * The performance could varied a lot in different time ranges.
    * `"volume_average_days"`
        * number of days of volume used to select the coins
    * `"test_portion"`
        * portion of backtest data, ranging from 0 to 1. The left is training data.
    * `"global_period"`
        * trading period and period of prices in input window.
        * should be a multiple of 300 (seconds)
    * `"coin_number"`
        * number of assets to be traded.
        * does not include cash (i.e. btc)
    * `"online"`
        * if it is not online, the program will select coins and generate inputs
        from the local database (at `database/Data.db`)
        * if it is online, new data that dose not exist in the database would be saved

#### Using SQlite

If you want to supply your own test data (or use downloaded ones), name the `SQLite` file `Data.db` and place it in the folder `database` (i.e. replace the downloaded `database/Data.db` file). Make sure that the table `history` has the same schema as the downloaded file. If you're not sure, run `python main.py --mode=download-data` and inspect the schema.

#### Using CSVs as Input

We added the option of allowing users to provide `.csv` market data instead of a `SQLite` file which we found to be unwieldy for manual generation and inspection.

We provided two tools: `csv_to_sqlite.py` and `sqlite_to_csv.py` that converts back and forth between `CSV` and `SQLite` data. To convert your own `CSV` file to the `SQLite` format to be consumed, do

```
python csv_to_sqlite.py --input=<path_to_your_input_csv>
```

By default, it will write to `database/Data.db`.

`sqlite_to_csv.py` is a convenience debugging tool for you to inspect the downloaded `SQLite` file easily and understand what columns you need for training.

Doing `csv_to_sqlite.py` then running the training procedure with `net_config.json`'s `online=False` will allow you to train the model using CSVs.

## Training and Tuning the hyper-parameters
1. First, modify the `nntrader/nntrader/net_config.json` file.
2. make sure current directory is under `nntrader` and type `python main.py --mode=generate --repeat=1`
    * this will make 1 subfolders under the `train_package`
    * in each subfolder, there is a copy of the `net_config.json`
    * `--repeat=n`, n could followed by any positive integers. The random seed of each the subfolder is from 0 to n-1 sequentially.
      * Notably, random seed could also affect the performance in a large scale.
3. type `python main.py --mode=train --processes=1`
    * this will start training one by one of the n folder created just now
    * do not start more than 1 processes if you want to download data online
    * "--processes=n" means start n processes running parallely.
    * add "--device=gpu" if your tensorflow support gpu.
      * On GTX1080Ti you should be able to run 4-5 training process together.
      * On GTX1060 you should be able to run 2-3 training together.
    * Each training process is made up from 2 stages:
      * Pre-training, log example:
      
      
```
INFO:root:average time for data accessing is 0.00070324587822
INFO:root:average time for training is 0.0032548391819
INFO:root:==============================
INFO:root:step 3000
INFO:root:------------------------------
INFO:root:the portfolio value on test set is 2.24213
log_mean is 0.00029086
loss_value is -0.000291
log mean without commission fee is 0.000378

INFO:root:==============================

```
        
        
      * Backtest with rolling train, log example:
```
        DEBUG:root:==============================
INFO:root:the step is 1433
INFO:root:total assets are 17.732482 BTC
```
4. after that, check the result summary of the training in `nntrader/train_package/train_summary.csv`
5. tune the hyper-parameters based on the summary, and go to 1 again.

## Logging
There are three types of logging of each training.
* In each subfolder
    * There is a text file called `programlog`, which is the log generated by the running programming.
    * There is a `tensorboard` folder saves the data about the training process which could be viewed by tensorboard.
        * type `tensorboard --logdir=train_package/1` to use tensorboard
* The summary infomation of this training, including network configuration, portfolio value on validation set and test set etc., will be saved in the `train_summary.csv` under `train_pakage` folder

## Save and Restore of the Model
* The trained weights of the network are saved at `train_package/1` named as `netfile` (including 3 files). 

## Download Data
* Type `python main.py --mode=download_data` you can download data without starting training
* The program will use the configurations in `nntrader/nntrader/net_config` to select coins and
  download necessary data to train the network.
* The downloading speed could be very slow and sometimes even have error in China.
* For those who cann't download data, please check the first release where there is a `Data.db` file, put it in the database folder. Make sure the `online` in `input` in `net_config.json` to be `false` and run the example.
  * Note that using the this file, you shouldn't make any changes to input data configuration(For example `start_date`, `end_date` or `coin_number`) otherwise incorrect result might be presented.
  
## Back-test
*Note: Before back-testing, you need to suceessfully finish training of algo first*
* Type `python main.py --mode=backtest --algo=1` to execute
backtest with rolling train(i.e. online learning in supervised learning)
on the target model.
* `--algo` could be either the name of traditional method or the index of training folder


## Plotting
* type `python main.py --mode=plot --algos=crp,olmar,1 --labels=crp,olmar,nnagent
`,for example, to plot
* `--algos` could be the name of the tdagent algorithms or
the index of nnagent
* `--labels` is the name of related algorithm that will be shown in the legend

## present backtest results in a table
* type `python main.py --mode=table --algos=1,olmar,ons --labels=nntrader,olmar,ons`
* `--algos` and `--lables` are the same as in plotting case
* result:
```
           average  max drawdown  negative day  negative periods  negative week  portfolio value  positive periods  postive day  postive week  sharpe ratio
nntrader  1.001311      0.225874           781              1378            114        25.022516              1398         1995          2662      0.074854
olmar     1.000752      0.604886          1339              1451           1217         4.392879              1319         1437          1559      0.035867
ons       1.000231      0.217216          1144              1360            731         1.770931              1416         1632          2045      0.032605

```
* use `--format` arguments to change the format of the table,
 could be `raw` `html` `csv` or `latex`. The default one is raw.
