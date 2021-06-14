# Flask example
### Install & run

```bash
pip3 install -r requirements.txt;
python3 app.py
```

\
You'll need to get your token from the [Nordigen's Open Banking Portal](https://ob.nordigen.com/login/)


##### 1. Go to http://localhost:8081/
<!-- ![acc token](../../../docs/resources/_media/f_1_token.png?raw=true "Title") -->
<p align="center">
    <img align="center" src="../../../docs/resources/_media/f_1_token.png" width="400" />
</p>
Enter access token and press enter



##### 2. Select Country
<!-- ![acc token](../../../docs/resources/_media/f_2_select_country.png?raw=true "Title") -->
<p align="center">
    <img align="center" src="../../../docs/resources/_media/f_2_select_country.png" width="200" />
</p>

##### 3. Select bank
<!-- ![acc token](../../../docs/resources/_media/f_3_select_aspsp.png?raw=true "Title") -->
<p align="center">
    <img align="center" src="../../../docs/resources/_media/f_3_select_aspsp.png" width="200" />
</p>

##### 4.1. Nordigen agreement
<p align="center">
  <img src="../../../docs/resources/_media/f_4_ng_agreement.jpg" width="200" />
  <img src="../../../docs/resources/_media/f_4.1_ng_redirect.png" width="200" /> 
</p>

##### 5. Sign into ASPSP
<p align="center">
  <img src="../../../docs/resources/_media/f_5_aspsps_signin.png" width="230" />
  <img src="../../../docs/resources/_media/f_5.1_aspsps_signin.jpg" width="200" /> 
  <img src="../../../docs/resources/_media/f_5.2_aspsps_signin.jpg" width="200" /> 
</p>

<p align="center">
  <img src="../../../docs/resources/_media/f_5.3_aspsp_auth.jpg" width="200" /> 
</p>

##### 6. Select accounts
<p align="center">
  <img src="../../../docs/resources/_media/f_6_aspsp_accs.jpg" width="200" />
</p>

##### 7. Download data
Here redirect from nordigen to http://localhost:8081/results?ref={ref_id} happens
<p align="center">
  <img src="../../../docs/resources/_media/f_7_accc_data.png" width="500" />
</p>
