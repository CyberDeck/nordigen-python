# Python requests example
### Install & run

```bash
pip3 install -r requirements.txt;
python3 main.py 
1. Visit: https://ob.nordigen.com/psd2/start/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/REVOLUT_REVOGB21
2. Authorise
And press Enter to continue...
```
Visit URL, agree, authorise into aspsp.
This will redirect you to: http://localhost/requisition?ref=xxx you can just ignore that.

After redirect to localhost - press enter.

```bash
And press Enter to continue... 
Get balances for account: bd2101c8-20fb-46fa-bc4b-85759faad817
Get balances for account: c2a17da9-0da3-4b72-a10e-10fee5c7f104
Get transactions for account: bd2101c8-20fb-46fa-bc4b-85759faad817
Get transactions for account: c2a17da9-0da3-4b72-a10e-10fee5c7f104
```
2 files (balances and transactions) for each account are saved in working directory.