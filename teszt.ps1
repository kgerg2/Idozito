Get-EventSubscriber | echo
Get-EventSubscriber | Unregister-Event
[void][System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
$balloon = New-Object System.Windows.Forms.NotifyIcon -Property @{
    Icon = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\clock-icon.ico"
    BalloonTipTitle = "Figyelmezteto"
    BalloonTipText = "A számítógépet már 50 perce használod folyamatosan.
Kattints ide, hogy alvó állapotba rakd!"
    Visible = $True
}
$balloon.ShowBalloonTip(1)
Register-ObjectEvent $balloon BalloonTipClosed -SourceIdentifier event_BalloonTipClosed
Register-ObjectEvent $balloon BalloonTipClicked -SourceIdentifier event_BalloonTipClicked
$retEvent = Wait-Event event_BalloonTip* -TimeOut 5
echo $retEvent
$retSourceIdentifier = $retEvent.SourceIdentifier
If ($retSourceIdentifier -eq "event_BalloonTipClicked"){ echo klikk }
# Unregister-Event -SourceIdentifier event_BalloonTipClicked
# Unregister-Event -SourceIdentifier event_BalloonTipClosed
$balloon.Dispose()
