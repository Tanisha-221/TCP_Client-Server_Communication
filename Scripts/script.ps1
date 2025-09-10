*Set Variables *
$resourceGroup = "T-ResourceGroup"              
$location = "westeurope"  
$VNetName = "MyVnet"
$SubnetName = "MySubnet"
$NSGName = "MyNSG"
$VMSize = "Standard_DS1_v2"
$VMNames = @("ServerVm1", "ClientVm2", "ClientVm3")

*Creating 3 VM 
foreach ($vmName in $VMNames) {
    New-AzVm `
        -ResourceGroupName $resourceGroup `
        -Name $vmName `
        -Location $location `
        -Image 'MicrosoftWindowsServer:WindowsServer:2022-datacenter-azure-edition:latest' `
        -VirtualNetworkName $VNetName `
        -SubnetName $SubnetName `
        -SecurityGroupName $NSGName `
        -PublicIpAddressName "$vmName-pip" `
        -OpenPorts 80,3389
}
    Start-Sleep -Seconds 30
