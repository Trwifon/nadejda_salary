function printTable() {
    const table = document.querySelector('.table-list');
    const title = document.querySelector('h5').innerText;
    
    // Create a hidden iframe for printing
    let printFrame = document.getElementById('printFrame');
    if (!printFrame) {
        printFrame = document.createElement('iframe');
        printFrame.id = 'printFrame';
        printFrame.style.position = 'absolute';
        printFrame.style.top = '-10000px';
        printFrame.style.left = '-10000px';
        document.body.appendChild(printFrame);
    }
    
    const printContent = `
        <html>
        <head>
            <title>Печат</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h5 { text-align: center; margin-bottom: 20px; }
                table { border-collapse: collapse; width: 100%; font-size: 10px; }
                th, td { border: 1px solid #000; padding: 4px; text-align: center; }
                th { background-color: #f0f0f0; }
                @media print {
                    @page { size: landscape; margin: 10mm; }
                }
            </style>
        </head>
        <body>
            <h5>${title}</h5>
            ${table.outerHTML}
        </body>
        </html>
    `;
    
    printFrame.contentDocument.open();
    printFrame.contentDocument.write(printContent);
    printFrame.contentDocument.close();
    
    printFrame.contentWindow.focus();
    printFrame.contentWindow.print();
}
