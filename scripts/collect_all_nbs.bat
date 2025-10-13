@echo off
echo Creating output directory if it doesn't exist...
if not exist "_collected_nbs\" mkdir "_collected_nbs"

echo Copying all .nbs files to output directory...
for /r %%f in (*.nbs) do (
    echo Copying: %%f
    copy "%%f" "_collected_nbs\"
)

echo Done! All .nbs files have been copied to the output folder.
echo Press any key to exit...
pause > nul