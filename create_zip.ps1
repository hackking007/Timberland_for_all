# Create ZIP file for GitHub upload
$zipPath = "C:\Users\moshele\Desktop\telegram-bot.zip"

# Remove existing ZIP if it exists
if (Test-Path $zipPath) { Remove-Item $zipPath }

# Create new ZIP
Add-Type -AssemblyName System.IO.Compression.FileSystem

$zip = [System.IO.Compression.ZipFile]::Open($zipPath, 'Create')

# Add files and folders
$basePath = "C:\Users\moshele\Desktop\TS1"

# Add .github folder
Get-ChildItem "$basePath\.github" -Recurse | ForEach-Object {
    $relativePath = $_.FullName.Substring($basePath.Length + 1)
    if (!$_.PSIsContainer) {
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $relativePath)
    }
}

# Add bot folder
Get-ChildItem "$basePath\bot" -Recurse | ForEach-Object {
    $relativePath = $_.FullName.Substring($basePath.Length + 1)
    if (!$_.PSIsContainer) {
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $relativePath)
    }
}

# Add individual files
@("README.md", "requirements.txt", "test_components.py") | ForEach-Object {
    $filePath = "$basePath\$_"
    if (Test-Path $filePath) {
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $filePath, $_)
    }
}

$zip.Dispose()

Write-Host "ZIP file created: $zipPath"
Write-Host "Upload this file to GitHub via web interface"