# AI-PCC Reporting Template

This work attempts to make a reporting template for MPEG AI PCC to analyze the testing results, such as calculating the BD-Rates, feawing the RD curves, etc.

## Requirments

```shell
pip install pandas matplotlib
```

We use the Bjontegaard metric calculation function from:
https://github.com/Anserw/Bjontegaard_metric/blob/master/bjontegaard_metric.py
Other resources are also available:
https://github.com/mauriceqch/pcc_geo_cnn/blob/master/src/metrics.py
https://www.mathworks.com/matlabcentral/fileexchange/27798-bjontegaard-metric


## Usages

```shell
python test.py --csvdir1='csvfiles/reporting_template_lossy.csv' --csvdir2='csvfiles/test.csv'  --xlabel='numBitsGeoEncT' --ylabel='d1T'
```

## Results

|Template    |python script  |G-PCC Excel  |
|------------|---------------|-------------|
|house_vox12 |-11.1          |-10.9        |


## Update

20220512: Test on csv files including more sequences, the csv files are provided by Muhammad.


## TODO

