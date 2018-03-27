import requests
import re
import os

user = ''
password = ''
baseurl = 'https://sanity.vodafone.co.nz/'

def get_leaf_from_tree(pageurl, leaflist):
 
  r = requests.get(baseurl + pageurl, auth=(user, password))

  if 'ip_tree.php' in r.text or 'subnet_tree.php' in r.text:
    leaflines = r.text.splitlines()

    for line in leaflines:
       if "ip_tree.php" in line:
          ips = re.findall('action="/(ip_tree.php\?subnet=[0-9]*)', line)
          for ip in ips:
             leaflist.append(ip)
          #leaflist.append(re.findall('action="/(ip_tree.php\?subnet=[0-9]*)', line))

       if "subnet_tree.php" in line:
          get_leaf_from_tree('\n'.join(re.findall('src="(/subnet_tree.php\?parent=[0-9]*)', line)), leaflist)           

#    leafs = re.findall('action="/(ip_tree.php\?subnet=[0-9]*)', r.text)
#    for leaf in leafs:
#      leaflist.append(leaf)  

#  if 'subnet_tree.php' in r.text:
#    tree = re.findall('src="(/subnet_tree.php\?parent=[0-9]*)', r.text)
#    for entry in tree:
#        get_leaf_from_tree(entry, leaflist) 

  return 
 
def get_ips(pageurl):
   r = requests.get(baseurl + pageurl, auth=(user, password))   

   hosts = []

   if 'tree.add' in r.text:
     #hostsblob = re.findall(r'tree.add\(new WebFXTreeItem\(\'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*/edit_host.php', r.text)

     hostslines = r.text.splitlines()

     for line in hostslines:
       if "edit_host.php" in line:
	 hosts.append(re.findall(r'WebFXTreeItem\(\'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', line))

   return hosts

r = requests.get(baseurl + 'user_ip_register.php', auth=(user, password))
if 'tree.add' in r.text:
     top_level = re.findall('tree.add\(new WebFXLoadTreeItem\(\'(.*)\', \'(.*)\'', r.text)
     for vrf in top_level:
	#make a directory for this VRF
	os.mkdir(vrf[0].replace('/', '.'))
        
	#walk the tree and get all the ip_tree.php entries
	r = requests.get(baseurl + vrf[1])
	subnets = []
        get_leaf_from_tree(vrf[1], subnets)

	#write a targets.txt file in the subdirectory
        f= open(vrf[0].replace('/', '.') + "/targets.txt","w+")

	#get the active IP's from the leafs
        for subnet in subnets:
	   ips=get_ips(subnet)

	   print("======= " + vrf[0] + " ========")
           print(ips)
 	   print('\n\n')
	

	   for ip in ips:
	     f.write('\n'.join(ip)+'\n')
	
	f.close()
