## Setup resource gropu name ,Vnet, Subnet and NSG with inbound rules 
```
RG="MyResourceGroup"
LOCATION="eastus"
VNET="MyVnet"
SUBNET="MySubnet"
NSG="MyNSG"

# Create resource group
az group create --name $RG --location $LOCATION

# Create virtual network and subnet
az network vnet create --resource-group $RG --name $VNET --address-prefix 10.0.0.0/16 \
  --subnet-name $SUBNET --subnet-prefix 10.0.1.0/24

# Create network security group
az network nsg create --resource-group $RG --name $NSG

# Allow SSH from your IP
YOUR_IP=$(curl -s ifconfig.me)/32
az network nsg rule create --resource-group $RG --nsg-name $NSG --name AllowSSH \
  --protocol Tcp --priority 1000 --destination-port-range 22 --access Allow \
  --direction Inbound --source-address-prefixes $YOUR_IP

# Allow traffic on port 5001 (app communication) from anywhere
az network nsg rule create --resource-group $RG --nsg-name $NSG --name AllowAppPortPublic \
  --protocol Tcp --priority 1010 --destination-port-ranges 5001 --access Allow \
  --direction Inbound --source-address-prefixes Internet
```
## Create 3 VMs with Public IP, Python installed via cloud-init
```
VMS=("vm1" "vm2" "vm3")
SSH_KEY_PATH="$HOME/.ssh/id_rsa.pub"
CLOUD_INIT_FILE="install-python.yaml"

for VMNAME in "${VMS[@]}"; do
  az vm create \
    --resource-group $RG \
    --name $VMNAME \
    --image Ubuntu2204 \
    --size Standard_B1s \
    --admin-username azureuser \
    --ssh-key-values "$(cat $SSH_KEY_PATH)" \
    --vnet-name $VNET \
    --subnet $SUBNET \
    --nsg $NSG \
    --custom-data $CLOUD_INIT_FILE
done
```
## Get Public IP Addresses of VMs
``` 
for VMNAME in "${VMS[@]}"; do
  PUB_IP=$(az vm list-ip-addresses -g $RG -n $VMNAME --query "[].virtualMachine.network.publicIpAddresses[0].ipAddress" -o tsv)
  echo "$VMNAME public IP: $PUB_IP"
done
```
## Upload Your 6 Local Python Files to Each VM Over Public IP
```
FILES=( multiservr.py clientserver.py serverfile.py clientfile.py heartbeats1.py heartbeatc1.py )
REMOTE_PATH="/home/azureuser/"
USER="azureuser"

for VMNAME in "${VMS[@]}"; do
  PUB_IP=$(az vm list-ip-addresses -g $RG -n $VMNAME --query "[].virtualMachine.network.publicIpAddresses[0].ipAddress" -o tsv)
  
  echo "Uploading files to $VMNAME at $PUB_IP"
  
  scp "${FILES[@]}" $USER@$PUB_IP:$REMOTE_PATH
done
```
## SSH Into Each VM and Run Your Server and Client Scripts
```
ssh azureuser@<vm-public-ip>

# Run your server on one VM:
python3 multiservr.py

# Run clients on other VMs:
python3 clientserver.py
# Or respective client/heartbeat scripts
```
