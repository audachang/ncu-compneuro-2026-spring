$ErrorActionPreference = "Stop"
$pptApp = New-Object -ComObject PowerPoint.Application

$format = 32 # ppSaveAsPDF
$files = Get-ChildItem -Path . -Filter *.pptx
foreach($file in $files) {
    if (-not $file.Name.StartsWith("~$")) {
        $pdfPath = [System.IO.Path]::ChangeExtension($file.FullName, ".pdf")
        Write-Host "Converting $($file.Name) to PDF..."
        $presentation = $pptApp.Presentations.Open($file.FullName)
        $presentation.SaveAs($pdfPath, $format)
        $presentation.Close()
    }
}
$pptApp.Quit()
Write-Host "All files converted successfully."
