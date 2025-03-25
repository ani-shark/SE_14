# Base URL for the API
$baseUrl = "http://localhost:5000"

# Function to make a POST request to the API
function Test-APIQuery {
    param (
        [string]$subject,
        [string]$query
    )
    $body = @{
        "subject" = $subject
        "query" = $query
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$baseUrl/query" -Method Post -Body $body -ContentType "application/json"
    return $response
}

# Test 1: Valid query for PDSA subject
Write-Host "Test 1: Valid query for PDSA subject"
$response = Test-APIQuery -subject "PDSA" -query "Where can I find information on string matching?"
Write-Host "Response: $($response.response)"

# Test 2: Valid query for another subject (replace with an actual subject in your system)
Write-Host "`nTest 2: Valid query for another subject"
$response = Test-APIQuery -subject "BDM" -query "What is ScatterPlot Analysis?"
Write-Host "Response: $($response.response)"

# Test 3: Query with missing subject
Write-Host "`nTest 3: Query with missing subject"
try {
    $body = @{
        "query" = "What is machine learning?"
    } | ConvertTo-Json
    Invoke-RestMethod -Uri "$baseUrl/query" -Method Post -Body $body -ContentType "application/json"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

# Test 4: Query with missing query
Write-Host "`nTest 4: Query with missing query"
try {
    $body = @{
        "subject" = "PDSA"
    } | ConvertTo-Json
    Invoke-RestMethod -Uri "$baseUrl/query" -Method Post -Body $body -ContentType "application/json"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}

# Test 5: Query for a topic not in the materials
Write-Host "`nTest 5: Query for a topic not in the materials"
$response = Test-APIQuery -subject "PDSA" -query "When is quantum computing covered?"
Write-Host "Response: $($response.response)"
