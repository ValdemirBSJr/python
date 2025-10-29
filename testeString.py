#code: utf-8
#Author: Valdemir Bezerra

texto=["http://vqr.virtua.com.br/call_detail.php?source=176779192&partition=vqr_summary_partition30&sel_switch=JPADTCDPI-01&schema_version=v766&fqdn=3486833",
       "http://vqr.virtua.com.br/call_detail.php?source=176779192&partition=vqr_summary_partition30&sel_switch=JPADTCDPI-01&schema_version=v766&fqdn=3486844"]


for i in texto:
    dividido = i.rsplit('fqdn=', 1)

    print(dividido[1])