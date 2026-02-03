$url = "https://github.com/NeoForgeMDKs/MDK-1.21.1-NeoGradle/archive/refs/heads/main.zip"
$zipFile = "neoforge-mdk.zip"
$extractFolder = "neoforge-temp"
$innerFolder = "MDK-1.21.1-NeoGradle-main" # Guessing based on repo name + branch

Write-Host "Starting NeoForge MDK Setup (Source: GitHub NeoForgeMDKs)..."

# Download
Write-Host "Downloading from $url..."
try {
    Invoke-WebRequest -Uri $url -OutFile $zipFile -ErrorAction Stop
} catch {
    Write-Error "Download failed: $_"
    exit 1
}

# Extract
Write-Host "Extracting..."
try {
    # Extract to a temp folder to avoid clutter if inner folder name is unexpected
    Expand-Archive -Path $zipFile -DestinationPath $extractFolder -Force -ErrorAction Stop
} catch {
    Write-Error "Extraction failed: $_"
    exit 1
}

# Move files
Write-Host "Moving files to current directory..."
try {
    # Find the actual inner folder name (in case it's not main or slightly different)
    $actualInner = Get-ChildItem -Path $extractFolder -Directory | Select-Object -First 1
    if ($actualInner) {
        $sourcePath = $actualInner.FullName + "\*"
        Move-Item -Path $sourcePath -Destination . -Force -ErrorAction Stop
        Write-Host "Moved files from $($actualInner.Name)"
    } else {
        Write-Error "Could not find inner folder in extracted archive."
    }
} catch {
    Write-Error "Move failed: $_"
    # Don't exit, try to clean up
}

# Cleanup
Write-Host "Cleaning up..."
Remove-Item -Path $zipFile -Force -ErrorAction SilentlyContinue
if (Test-Path $extractFolder) { Remove-Item -Path $extractFolder -Recurse -Force -ErrorAction SilentlyContinue }

$uselessFiles = @("CHANGELOG.md", "CHANGELOG.txt", "LICENSE.txt", "README.txt", "CREDITS.txt", "license.txt", "readme.txt", "README.md")
foreach ($file in $uselessFiles) {
    if (Test-Path $file) {
        Remove-Item -Path $file -Force
        Write-Host "Removed $file"
    }
}

# List files
Write-Host "`nInstallation complete. File list:"
Get-ChildItem | Format-Table -AutoSize