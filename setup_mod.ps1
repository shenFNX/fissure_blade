# 1. Variables
$modId = "fissure_blade"
$modName = "Fissure Blade"
$author = "shen_FNX"
$basePkg = "com.shen.fissureblade"
$oldPkg = "com.example.examplemod"
$group = "com.shen"

Write-Host "Starting Mod Setup for '$modName' ($modId)..."

# 2. Update gradle.properties (This is where the actual ID/Name are defined in this template)
$gradlePropsPath = "gradle.properties"
if (Test-Path $gradlePropsPath) {
    $content = Get-Content $gradlePropsPath -Raw
    $content = $content -replace "mod_id=examplemod", "mod_id=$modId"
    $content = $content -replace "mod_name=Example Mod", "mod_name=$modName"
    $content = $content -replace "mod_group_id=com.example.examplemod", "mod_group_id=$basePkg"
    # Note: Author is not standard in gradle.properties for this template, but we updated the main ones.
    Set-Content -Path $gradlePropsPath -Value $content
    Write-Host "Updated gradle.properties"
}

# 3. Refactor Java Packages
$oldPath = "src/main/java/com/example/examplemod"
$newPath = "src/main/java/com/shen/fissureblade"

if (Test-Path $oldPath) {
    if (-not (Test-Path $newPath)) {
        New-Item -ItemType Directory -Force -Path $newPath | Out-Null
    }
    
    # Move all files
    Get-ChildItem -Path $oldPath | Move-Item -Destination $newPath -Force
    
    # Clean up old empty folders (example/examplemod)
    Remove-Item -Path "src/main/java/com/example" -Recurse -Force -ErrorAction SilentlyContinue
    
    Write-Host "Moved source files to $newPath"
}

# 4. Update Java Files Content
$javaFiles = Get-ChildItem -Path $newPath -Filter "*.java"
foreach ($file in $javaFiles) {
    $c = Get-Content $file.FullName -Raw
    
    # Replace package
    $c = $c -replace "package $oldPkg;", "package $basePkg;"
    
    # If it's the main class (ExampleMod.java)
    if ($file.Name -eq "ExampleMod.java") {
        $c = $c -replace 'MODID = "examplemod"', "MODID = `"$modId`""
        $c = $c -replace 'class ExampleMod', "class FissureBlade"
        $c = $c -replace 'public ExampleMod', "public FissureBlade"
        $c = $c -replace 'ExampleMod.MODID', "FissureBlade.MODID"
    }
    
    Set-Content -Path $file.FullName -Value $c
}

# 5. Rename Main Class File
$mainJava = Join-Path $newPath "ExampleMod.java"
if (Test-Path $mainJava) {
    Rename-Item -Path $mainJava -NewName "FissureBlade.java"
    Write-Host "Renamed ExampleMod.java to FissureBlade.java"
}

Write-Host ">>> [Success] Mod renamed to: $modName ($modId) <<<" -ForegroundColor Green
