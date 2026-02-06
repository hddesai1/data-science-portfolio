# Script to migrate repository to a new remote
# Usage: .\migrate-to-new-repo.ps1 -NewRepoUrl "https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"

param(
    [Parameter(Mandatory=$true)]
    [string]$NewRepoUrl,
    
    [Parameter(Mandatory=$false)]
    [string]$BranchName = "master"
)

Write-Host "Starting repository migration..." -ForegroundColor Green
Write-Host ""

# Step 1: Remove old remote
Write-Host "Step 1: Removing old remote..." -ForegroundColor Yellow
try {
    $oldRemote = git remote get-url origin 2>$null
    if ($oldRemote) {
        Write-Host "  Current remote: $oldRemote" -ForegroundColor Gray
        git remote remove origin
        Write-Host "  ✓ Old remote removed" -ForegroundColor Green
    } else {
        Write-Host "  No existing remote found" -ForegroundColor Gray
    }
} catch {
    Write-Host "  No existing remote to remove" -ForegroundColor Gray
}

Write-Host ""

# Step 2: Add new remote
Write-Host "Step 2: Adding new remote..." -ForegroundColor Yellow
Write-Host "  New remote URL: $NewRepoUrl" -ForegroundColor Gray
git remote add origin $NewRepoUrl
Write-Host "  ✓ New remote added" -ForegroundColor Green

Write-Host ""

# Step 3: Verify remote
Write-Host "Step 3: Verifying remote configuration..." -ForegroundColor Yellow
git remote -v
Write-Host "  ✓ Remote verified" -ForegroundColor Green

Write-Host ""

# Step 4: Push to new repository
Write-Host "Step 4: Pushing to new repository..." -ForegroundColor Yellow
Write-Host "  This may prompt for authentication..." -ForegroundColor Gray
Write-Host ""

try {
    git push -u origin $BranchName
    Write-Host ""
    Write-Host "  ✓ Successfully pushed to new repository!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Migration completed successfully!" -ForegroundColor Green
    Write-Host "Your repository is now connected to: $NewRepoUrl" -ForegroundColor Cyan
} catch {
    Write-Host ""
    Write-Host "  ✗ Push failed. Please check:" -ForegroundColor Red
    Write-Host "    1. Repository URL is correct" -ForegroundColor Yellow
    Write-Host "    2. You have write access to the repository" -ForegroundColor Yellow
    Write-Host "    3. Your authentication credentials are set up" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You can manually push later with: git push -u origin $BranchName" -ForegroundColor Gray
}
