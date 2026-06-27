function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function printPaySlips() {
    const table = document.querySelector('.table-list');
    const title = document.querySelector('h5').innerText;
    const dataRows = Array.from(table.querySelectorAll('tbody tr'));

    let printFrame = document.getElementById('printFrame');
    if (!printFrame) {
        printFrame = document.createElement('iframe');
        printFrame.id = 'printFrame';
        printFrame.style.position = 'absolute';
        printFrame.style.top = '-10000px';
        printFrame.style.left = '-10000px';
        document.body.appendChild(printFrame);
    }

    const slips = dataRows.map((row) => {
        const cells = row.querySelectorAll('td');

        return {
            name: cells[0].innerText.trim(),
            workshop: cells[1].innerText.trim(),
            mainSalary: cells[2].innerText.trim(),
            bonusBoss: cells[3].innerText.trim(),
            bonusConstant: cells[4].innerText.trim(),
            bonusVariable: cells[5].innerText.trim(),
            totalSalary: cells[6].innerText.trim(),
            days: cells[7].innerText.trim(),
            salaryEarned: cells[8].innerText.trim(),
            sickDaysSum: cells[9].innerText.trim(),
            payForVacation: cells[10].innerText.trim(),
            total: cells[11].innerText.trim(),
            unpaidHoursEuro: cells[12].innerText.trim(),
            bank: cells[13].innerText.trim(),
            cash: cells[14].innerText.trim(),
            mobile: cells[15].innerText.trim(),
            voucher: cells[16].innerText.trim(),
            rest: cells[17].innerText.trim(),
        };
    });

    const slipGroups = [];
    for (let index = 0; index < slips.length; index += 12) {
        slipGroups.push(slips.slice(index, index + 12));
    }

    const printContent = `
        <html>
        <head>
            <title>Фишове</title>
            <style>
                :root {
                    --border: 1px solid #111;
                }

                html, body {
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                    color: #111;
                }

                body {
                    padding: 4mm;
                }

                .page {
                    page-break-after: always;
                    break-after: page;
                }

                .page:last-child {
                    page-break-after: auto;
                    break-after: auto;
                }

                .slip-grid {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 0.2mm;
                }

                .slip {
                    border: var(--border);
                    padding: 2mm;
                    min-height: 26mm;
                    box-sizing: border-box;
                    font-size: 9px;
                    line-height: 1.25;
                }

                .slip-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: baseline;
                    gap: 4mm;
                    padding-bottom: 2mm;
                    margin-bottom: 2mm;
                    border-bottom: var(--border);
                }

                .slip-name {
                    font-size: 11px;
                    font-weight: 700;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                }

                .slip-meta {
                    font-size: 8px;
                    white-space: nowrap;
                }

                .slip-table {
                    width: 100%;
                    border-collapse: collapse;
                }

                .slip-table td {
                    padding: 0.7mm 0;
                    vertical-align: top;
                }

                .slip-label {
                    width: 58%;
                    padding-right: 3mm;
                }

                .slip-value {
                    width: 42%;
                    text-align: right;
                    font-weight: 700;
                    white-space: nowrap;
                }

                .slip-total {
                    margin-top: 2mm;
                    padding-top: 2mm;
                    border-top: var(--border);
                    font-size: 10px;
                    font-weight: 700;
                }

                @page {
                    size: A4 portrait;
                    margin: 4mm;
                }

                @media print {
                    body {
                        padding: 0;
                    }

                    .page {
                        min-height: calc(100vh - 8mm);
                    }
                }
            </style>
        </head>
        <body></body>
        </html>
    `;

    printFrame.onload = () => {
        const printDocument = printFrame.contentDocument;
        const printBody = printDocument.body;

        slipGroups.forEach((group) => {
            const page = printDocument.createElement('section');
            page.className = 'page';

            const grid = printDocument.createElement('div');
            grid.className = 'slip-grid';

            group.forEach((slip) => {
                const card = printDocument.createElement('article');
                card.className = 'slip';

                const header = printDocument.createElement('div');
                header.className = 'slip-header';
                header.innerHTML = `
                    <span class="slip-name">${escapeHtml(slip.name)}</span>
                    <span class="slip-meta">${escapeHtml(slip.workshop)}</span>
                `;

                const table = printDocument.createElement('table');
                table.className = 'slip-table';
                table.innerHTML = `
                    <tbody>
                        <tr><td class="slip-label">Осн. заплата</td><td class="slip-value">${escapeHtml(slip.mainSalary)}</td></tr>
                        <tr><td class="slip-label">Бонус шеф</td><td class="slip-value">${escapeHtml(slip.bonusBoss)}</td></tr>
                        <tr><td class="slip-label">Бонус пост.</td><td class="slip-value">${escapeHtml(slip.bonusConstant)}</td></tr>
                        <tr><td class="slip-label">Бонус пром.</td><td class="slip-value">${escapeHtml(slip.bonusVariable)}</td></tr>
                        <tr><td class="slip-label">Общо заплата</td><td class="slip-value">${escapeHtml(slip.totalSalary)}</td></tr>
                        <tr><td class="slip-label">Дни</td><td class="slip-value">${escapeHtml(slip.days)}</td></tr>
                        <tr><td class="slip-label">Сума</td><td class="slip-value">${escapeHtml(slip.salaryEarned)}</td></tr>
                        <tr><td class="slip-label">Болн. сума</td><td class="slip-value">${escapeHtml(slip.sickDaysSum)}</td></tr>
                        <tr><td class="slip-label">Отп. сума</td><td class="slip-value">${escapeHtml(slip.payForVacation)}</td></tr>
                        <tr><td class="slip-label">Общо запл.</td><td class="slip-value">${escapeHtml(slip.total)}</td></tr>
                        <tr><td class="slip-label">Непл. час. лв</td><td class="slip-value">${escapeHtml(slip.unpaidHoursEuro)}</td></tr>
                        <tr><td class="slip-label">Банка</td><td class="slip-value">${escapeHtml(slip.bank)}</td></tr>
                        <tr><td class="slip-label">Аванс</td><td class="slip-value">${escapeHtml(slip.cash)}</td></tr>
                        <tr><td class="slip-label">GSM</td><td class="slip-value">${escapeHtml(slip.mobile)}</td></tr>
                        <tr><td class="slip-label">Ваучер</td><td class="slip-value">${escapeHtml(slip.voucher)}</td></tr>
                    </tbody>
                `;

                const total = printDocument.createElement('div');
                total.className = 'slip-total';
                total.textContent = `За плащане: ${slip.rest}`;

                card.appendChild(header);
                card.appendChild(table);
                card.appendChild(total);
                grid.appendChild(card);
            });

            page.appendChild(grid);
            printBody.appendChild(page);
        });

        printFrame.contentWindow.focus();
        printFrame.contentWindow.print();
    };

    printFrame.srcdoc = printContent;
}
