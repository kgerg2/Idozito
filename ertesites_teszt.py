import subprocess

szkript = f"""[void][System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

$Title = "Cím"
$Text = "Szöveg"
$EventTimeOut = 5

$balloon = New-Object System.Windows.Forms.NotifyIcon -Property @{{
    Icon = "C:\\Users\\kgerg\\Documents\\GitHub\\Idozito\\clock-icon.ico"
    BalloonTipTitle = $Title
    BalloonTipText = $Text
    Visible = $True
}}

# Value "1" here is meaningless. $EventTimeOut will force bubble to close.
$balloon.ShowBalloonTip(1)

Register-ObjectEvent $balloon BalloonTipClicked -SourceIdentifier event_BalloonTipClicked
Register-ObjectEvent $balloon BalloonTipClosed -SourceIdentifier event_BalloonTipClosed

# "Wait-Event" pauses the script here until an event_BalloonTip* is triggered
# TimeOut is necessary or balloon and script hangs there forever. 
# This could be okay but event subscription gets messed up by following script instances generating the same event names1.
$retEvent = Wait-Event event_BalloonTip* -TimeOut $EventTimeOut

# Script resumes here.
$retSourceIdentifier = $retEvent.SourceIdentifier

If ($retSourceIdentifier -eq "event_BalloonTipClicked"){{
    echo klikk
}}

# Gets rid of icon. This is absolutely necessary, otherwise icon is stuck event if parent script/shell closes
$balloon.Dispose()

"""

eredm = subprocess.run(["powershell", szkript], stdout=subprocess.PIPE)
print("kész")
print(eredm.stdout)