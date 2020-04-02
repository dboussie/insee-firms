from google.cloud import bigquery
import requests
import json

def query_pa():
    #Select query for SIRET list
    client = bigquery.Client()
    query_job = client.query("""
        SELECT *
          FROM `billing-module-qa.partners_applications.partners_applications`
          LIMIT 10000""")

    results = query_job.result()  # Waits for job to complete.

	# Parse results
    for row in results:
        print("{}".format(row.SIRET))

        #INSEE SIREN API CALL
        
        url = 'https://api.insee.fr/entreprises/sirene/V3/siret/%s?champs=trancheEffectifsEtablissement&date=2020-03-24' % (row.SIRET)
        #print("{}".format(url))
        response = requests.get(url, headers = {'Authorization': 'Bearer c0678066-bcb0-35f4-8cc5-eecc4ca58afd'})
        
        if format(response) != "<Response [200]>" : print("Erreur : {}".format(response))
        else: 
        
          jsonResponse = response.json()
          tranche = jsonResponse.get('etablissement')
          effectif = tranche.get('trancheEffectifsEtablissement')
          if effectif is None : effectif = '00'
          print "Value : %s" %  effectif
  
          #SQL INSERT QUERY
          client = bigquery.Client()
          query = """
              UPDATE `billing-module-qa.partners_applications.partners_applications`
                  SET effectif = @effectif where SIRET = @siret
              """
		 
          job_config = bigquery.QueryJobConfig(
              query_parameters=[
                  bigquery.ScalarQueryParameter("effectif", "STRING", effectif),
                  bigquery.ScalarQueryParameter("siret", "INT64", row.SIRET),
              ]
          )
          query_job2 = client.query(query, job_config=job_config)
          results2 = query_job2.result()  # Waits for job to complete.

if __name__ == '__main__':
    query_pa()
	
	
#Token : c0678066-bcb0-35f4-8cc5-eecc4ca58afd	