[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

$objNotifyIcon = New-Object System.Windows.Forms.NotifyIcon

$objNotifyIcon.Icon = "C:\Users\kgerg\Documents\GitHub\Idozito\clock-icon.ico"
$objNotifyIcon.BalloonTipText = "Szöveg"
$objNotifyIcon.BalloonTipTitle = "Cím"

$objNotifyIcon.Visible = $True
$objNotifyIcon.ShowBalloonTip(10000)

[void] (Register-ObjectEvent -InputObject $objNotifyIcon -EventName BalloonTipClicked -Action {
#Perform cleanup actions on balloon tip
C:\Users\kgerg\Documents\Programok\nircmd.exe dlg
$objNotifyIcon.dispose()
#return 1
})

Register-ObjectEvent -InputObject $objNotifyIcon -EventName BalloonTipClosed -SourceIdentifier "Closed2"
Wait-Event -SourceIdentifier "Closed" -Timeout 10

<# C:\Users\kgerg\Documents\Programok\nircmd.exe #>
