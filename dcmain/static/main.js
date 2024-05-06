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
      let txnObjSel = document.getElementById('other_party_id');
      let txnModeSel = document.getElementById('transaction_mode');

      txnObjSel.innerHTML = '';
      txnModeSel.innerHTML = '';

      let modeOptions = [
        `${lcl.credit_transaction}.Credit To Dector`,
        `${lcl.credit_payment}.Pay From Dector`,
        `${lcl.debt_transaction}.Debt To Creditor`,
        `${lcl.debt_payment}.Pay To Creditor`,
      ];

      // let modeOpt1 = document.createElement('option');
      // let modeOpt2 = document.createElement('option');

      if (target.value === `${ccl.DEBTOR}`) {
        for (let indx in modeOptions.slice(0, 2)) {
          let newOpt = document.createElement('option');
          [newOpt.value, newOpt.innerHTML] = modeOptions[indx].split('.');
          txnModeSel.options.add(newOpt);
        }
      } else if (target.value === `${ccl.CREDITOR}`) {
        for (let indx in modeOptions.slice(2, 3)) {
          let newOpt = document.createElement('option');
          [newOpt.value, newOpt.innerHTML] = modeOptions[indx].split('.');
          txnModeSel.options.add(newOpt);
        }
      } else {
        // DO NOTHING as the inputs are already reset above
      }
    }
  });
}
