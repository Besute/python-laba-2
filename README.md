<h1>Python JSONL and CSV analyzer</h1>
<h3>With this package you can check fully analyze your data:</h3>
<ul>
    <li style="color: rgba(16, 185, 129, 1); font-size: 16px">Count number of events</li>
    <li style="color: rgba(16, 185, 129, 1); font-size: 16px">See TOP-5 sources of your error</li>
    <li style="color: rgba(16, 185, 129, 1); font-size: 16px">Count number of events</li>
    <li style="color: rgba(16, 185, 129, 1); font-size: 16px">See the lowest and the biggest time-label</li>
    <li style="color: rgba(16, 185, 129, 1); font-size: 16px">And other useful statistics...</li>
</ul>

<h2>Usage:</h2>
<h3>Note that you need to have these obligatory fields with strict formats:</h3>
<ol>
    <li style="color: rgba(239, 68, 68, 1); font-size: 16px">timestamp in ISO 8601 format</li>
    <li style="color: rgba(239, 68, 68, 1); font-size: 16px">level: [DEBUG | INFO | WARNING | ERROR | CRITICAL]</li>
    <li style="color: rgba(239, 68, 68, 1); font-size: 16px">source: length of source string must be at least 1</li>
    <li style="color: rgba(239, 68, 68, 1); font-size: 16px">message: could be any string</li>
</ol>
<p style="font-size: 16px">Use "python -m streamstats analyze [--FILENAMES...] --format (csv/jsonl)"</p>
<p style="font-size: 16px">this code will analyze your data and report it to output/REPORT.json inside the project. However, if you have
some errors in obligatory fields, the program won't finish analizing and will finish with error</p>
<h3>Flags</h3>
<p style="font-size: 16px">To set validation of obligatory fields use "--skip-valid" flag</p>
<p style="font-size: 16px">To set your report destination use "--output PATH" flag</p>
<h2>Setup</h2>
<p style="font-size: 16px">Use poetry for this package. You can install it in browser
or directly in your IDE</p>
<p style="font-size: 16px">Run "poetry install" to install the package</p>
<p style="font-size: 16px">Run "poetry sync" to sync all dependencies to the required version</p>
<h2>Additional</h2>
<p style="font-size: 16px">You can fork this project and add new
format to be analyzed. To do that go to src/streamstats/EventService/base_for_event.py to see skeleton of file what is needed to be written</p>
<p style="font-size: 16px">Then go to the parsers and add you new analyzer to the EVENT by given function</p>
<p style="font-size: 16px">!NOTE! Your parses should do the special format that other parsers do. You can see it by printing them in the server's file</p>