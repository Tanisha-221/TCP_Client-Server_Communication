## Powershell script to create 3Vm 
* Set Variables
```
$resourceGroup = "TA-ResourceGroup"               
$location = "westeurope"   
$VNetName = "MyVnet"
$SubnetName = "MySubnet"
$NSGName = "MyNSG"
$VMSize = "Standard_DS1_v2"
$VMNames = @("ServerVm1", "ClientVm2", "ClientVm3")
```
* Step1: Create a new resource Group 
``` 
New-AzResourceGroup -ResourceGroupName "TA-ResourceGroup" -Location "westeurope"
```
* Set Credential 
```
$cred = Get-Credential
"PowerShell credential request
Enter your credentials.
User: Tanisha 
Password for user Tanisha: ************"
```
* Step 2: Create Virtual Network and Subnet
```
$SubnetConfig = New-AzVirtualNetworkSubnetConfig -Name $SubnetName -AddressPrefix "10.0.1.0/24"
$VNet = New-AzVirtualNetwork -ResourceGroupName $resourceGroup -Location $Location `
    -Name $VNetName -AddressPrefix "10.0.0.0/16" -Subnet $SubnetConfig
```    
* Step 2: Create a static public IP address without DNS label (to avoid parameter issues)
```
$publicIpName = "mypublicip$(Get-Random)"

$pip = New-AzPublicIpAddress -ResourceGroupName $resourceGroup `
                             -Location $location `
                             -Name $publicIpName `
                             -AllocationMethod Static `
                             -IdleTimeoutInMinutes 4
```
* Step 3: Wait a bit to allow Azure to allocate the IP
```
Start-Sleep -Seconds 10
```

* Step 4: Retrieve the public IP resource to get assigned IP address
```
$pip = Get-AzPublicIpAddress -ResourceGroupName $resourceGroup -Name $publicIpName

Write-Output "Public IP Resource Created:"
Write-Output "Name: $publicIpName"
Write-Output "IP Address: $($pip.IpAddress)"
Write-Output "DNS Name: $($pip.DnsSettings.Fqdn)"  # Will be empty if DNS not set
```
* Create NSG rule for inbound RDP with descriptive name
```
$nsgRuleRDP = New-AzNetworkSecurityRuleConfig `
           -Name "Allow-RDP-Inbound" `
           -Protocol Tcp `
           -Direction Inbound `
           -Priority 1000 `
           -SourceAddressPrefix * `
           -SourcePortRange * `
           -DestinationAddressPrefix * `
           -DestinationPortRange 3389 `
           -Access Allow

# Create NSG named for resource group and its purpose
$nsg = New-AzNetworkSecurityGroup `
            -ResourceGroupName $resourceGroup `
            -Location $location `
            -Name "NSG-$resourceGroup-RDP" `
            -SecurityRules $nsgRuleRDP

# Create NIC with naming based on VM/project
$nic = New-AzNetworkInterface `
              -Name "NIC-$($VMNames[0])" `
              -ResourceGroupName $resourceGroup `
              -Location $location `
              -SubnetId $vnet.Subnets[0].Id `
              -PublicIpAddressId $pip.Id `
              -NetworkSecurityGroupId $nsg.Id
```              
* Create a virtual machine configuration
```
$vmConfig = New-AzVMConfig -VMName $vmName `
                     -VMSize Standard_D1 | `
            Set-AzVMOperatingSystem `
                     -Windows -ComputerName `
                     $vmName -Credential $cred | `
            Set-AzVMSourceImage `
                     -PublisherName MicrosoftWindowsServer `
                     -Offer WindowsServer `
                     -Skus 2016-Datacenter `
                     -Version latest | `
            Add-AzVMNetworkInterface -Id $nic.Id
```
* Inline script to install Python silently
```
$installPythonScript = @"
Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'C:\pythoninstaller.exe';
Start-Process -FilePath 'C:\pythoninstaller.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait;
Remove-Item 'C:\pythoninstaller.exe';
"@
```
* Creating 3Vm and install python 
```
foreach ($vmName in $VMNames){
New-AzVM -ResourceGroupName $resourceGroup -Location $location -VM $vmConfig

    # Install Python
    Set-AzVMCustomScriptExtension -ResourceGroupName $resourceGroup -VMName $vmName -Name "InstallPython" `
        -Location $location -Run "powershell -Command $installPythonScript"
}
```
