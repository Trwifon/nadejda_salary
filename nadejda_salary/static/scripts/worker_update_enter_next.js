document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('worker-update-form');
    const nextButton = document.getElementById('next-button');
    const bonusVariableField = document.getElementById('id_bonus_variable');

    if (bonusVariableField && !bonusVariableField.disabled && !bonusVariableField.readOnly) {
        bonusVariableField.focus();

        if (typeof bonusVariableField.select === 'function') {
            setTimeout(function () {
                bonusVariableField.select();
            }, 0);
        }
    }

    if (!form || !nextButton) {
        return;
    }

    form.addEventListener('keydown', function (event) {
        if (event.key !== 'Enter') {
            return;
        }

        if (event.target && event.target.tagName === 'TEXTAREA') {
            return;
        }

        event.preventDefault();
        nextButton.click();
    });
});
