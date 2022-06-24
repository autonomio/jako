# Data Visualisation API   

While the experiment is running, the user can access the round results and make visualisations and charts using the Metabase API. The postgres database should be connected to the metabase, and then the user can make visualisations by asking [metabase questions](https://www.metabase.com/docs/latest/users-guide/04-asking-questions.html).   


## Add metabase to your experiment
Add a key named `metabase` and set its value to `True` in the config.   

```
"metabase": "True"
```   

And include the config while running DistributeScan.   

```python
jako.DistributedScan(x='x', y='y', params=p, model=input_model,config='config.json')
```   

## Adding Data source to Metabase   

When you are running a DistributedScan experiment, the metabase window opens automatically in your browser.The url will be 'http://DB_HOST:3000', where `DB_HOST` is the host id of the remote machine which is used as centralised datastore.

If you are setting up metabase for the first time, then the url above will lead you to a setup page. Choose your language, and give the details as shown.   

In the section `Add Data`, the details to the centralised datastore should be given. Choose `PostgreSQL`, and fill the following as per instructions given below:   

* Display Name : You can give a custom name for the database 
* Host: Host is the host ip address of the centralised datastore. Refer config to find which machine the centralised datastore is running, and copy paste the host id from there.   
* Port: Database Port in Centralised Datastore. Default `5432`.
* Database name: Database Name in Centralised Datastore. Default `postgres`.   
* Username : Database Username in Centralised Datastore. Default `postgres`.
* Password : Database Password in Centralised Datastore. Default `postgres`.


Finish the next steps, and you got your data source connected to metabase for visualisations! Now go to `Browse data` section and do your custom visualisations.
