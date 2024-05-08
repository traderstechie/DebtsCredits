// SWITCH ACTIVE BUTTON IN COLLECTION
const switchActiveBtnInCollection = function (collectionClass, btn2Activate) {
  document.querySelectorAll(collectionClass).forEach((btn) => {
    if (btn === btn2Activate) {
      return btn.classList.contains('active') ? btn.classList.remove('active') : btn.classList.add('active');
    } else {
      return btn.classList.remove('active');
    }
  });
};

// DISPLAY MORE-OPTIONS-ARTICLE/DIV SELECTED-OPTION CONTENT
const displayMoreOptionsOptContent = function (clickTarget) {
  let container = clickTarget.parentNode;
  let targetContent = container?.querySelector(`${clickTarget.dataset.target}`);
  if (!targetContent) return;
  container.querySelectorAll('.moreOptionContent').forEach((tc) => {
    if (tc === targetContent) {
      return tc.hasAttribute('hidden') ? tc.removeAttribute('hidden') : tc.setAttribute('hidden', true);
    } else {
      return tc.setAttribute('hidden', true);
    }
  });
  // ...
  switchActiveBtnInCollection('.moreOptionAnchor', clickTarget);
};

// CLICK listeners WITHIN home page
if (typeof home_page !== 'undefined') {
  document.getElementById('home_page').addEventListener('click', function (e) {
    let target = e.target;
    if (!target) return;

    // .moreOptionsArticle.moreOptionAnchor
    if (target.classList.contains('moreOptionAnchor')) {
      displayMoreOptionsOptContent(target);

      // .moreOptionsArticle.moreOptionAnchor
    } else if (target.parentNode.classList.contains('moreOptionAnchor')) {
      displayMoreOptionsOptContent(target.parentNode);
    }
  });

  document.getElementById('home_page').addEventListener('change', function (e) {
    let target = e.target;
    if (!target) return;

    if (target.name === 'object_type') {
      let txnModeSel = document.getElementById('transaction_mode');
      let txnObjLabel = document.getElementById('other_party_id_label');

      txnModeSel.innerHTML = '';

      // Set first "empty" option for txn mode
      let newOpt = document.createElement('option');
      [newOpt.value, newOpt.innerHTML] = ['', 'Select'];
      txnModeSel.options.add(newOpt);

      /*
      Using this much simpler array and doing
      `for (let indx in modeOptions.slice())`
      was returning the first two items when
      `2, 4` or `-2` is passed to `slice` for 
      the `(target.value === `${ccl.CREDITOR}`)`
      So, I'll get back to it in the future
      const modeOptions = [
        `${lcl.credit_transaction}.Money To Debtor`,
        `${lcl.credit_payment}.Payment From Debtor`,
        `${lcl.debt_transaction}.Money From Creditor`,
        `${lcl.debt_payment}.Payment To Creditor`,
      ];
      */

      const debtorModeOptions = [
        `${lcl.credit_transaction}.Money To Debtor`,
        `${lcl.credit_payment}.Payment From Debtor`,
      ];

      const creditorModeOptions = [
        `${lcl.debt_transaction}.Money From Creditor`,
        `${lcl.debt_payment}.Payment To Creditor`,
      ];

      if (target.value === `${ccl.DEBTOR}`) {
        debtorModeOptions.forEach((opt) => {
          let newOpt = document.createElement('option');
          [newOpt.value, newOpt.innerHTML] = opt.split('.');
          txnModeSel.options.add(newOpt);
        });

        txnObjLabel.innerHTML = `Debtor ID <br> <small><em>(Copy one from Debtors list)</em></small>`;
      } else if (target.value === `${ccl.CREDITOR}`) {
        creditorModeOptions.forEach((opt) => {
          let newOpt = document.createElement('option');
          [newOpt.value, newOpt.innerHTML] = opt.split('.');
          txnModeSel.options.add(newOpt);

          txnObjLabel.innerHTML = `Creditor ID <br> <small><em>(Copy one from Creditors list)</em></small>`;
        });
      } else {
        txnModeSel.innerHTML = '';
        txnObjLabel.innerHTML = 'Txn Object';
      }
    }
  });
}
