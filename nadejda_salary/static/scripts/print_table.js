function printTable() {
    const table = document.querySelector('.table-list');
    const title = document.querySelector('h5').innerText;
    const headerCells = Array.from(table.querySelectorAll('thead th')).map((cell) => cell.textContent.trim());
    const dataRows = Array.from(table.querySelectorAll('tbody tr'));
    
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
                .print-header-row th { background-color: #f0f0f0; font-weight: 700; }
                .print-header-row,
                .print-data-row { break-inside: avoid; page-break-inside: avoid; }
                @media print {
                    @page { size: landscape; margin: 10mm; }
                }
            </style>
        </head>
        <body></body>
        </html>
    `;
    
    printFrame.contentDocument.open();
    printFrame.contentDocument.write(printContent);
    printFrame.contentDocument.close();

    const printDocument = printFrame.contentDocument;
    const printBody = printDocument.body;

    const heading = printDocument.createElement('h5');
    heading.textContent = title;
    printBody.appendChild(heading);

    const printTable = printDocument.createElement('table');
    const printTbody = printDocument.createElement('tbody');

    dataRows.forEach((row) => {
        const headerRow = printDocument.createElement('tr');
        headerRow.className = 'print-header-row';

        headerCells.forEach((label) => {
            const headerCell = printDocument.createElement('th');
            headerCell.textContent = label;
            headerRow.appendChild(headerCell);
        });

        const dataRow = printDocument.createElement('tr');
        dataRow.className = 'print-data-row';
        dataRow.innerHTML = row.innerHTML;

        printTbody.appendChild(headerRow);
        printTbody.appendChild(dataRow);
    });

    printTable.appendChild(printTbody);
    printBody.appendChild(printTable);
    
    printFrame.contentWindow.focus();
    printFrame.contentWindow.print();
}
