

export default function getNPV(rate, initialCost, cashFlows) {
    let npv = initialCost;
  
    for (let i = 0; i < cashFlows.length; i++) {
      npv += cashFlows[i] / Math.pow(rate / 100 + 1, i + 1);
    }
    const formattedNPV = npv.toLocaleString('en-US', { style: 'currency', currency: 'USD' }, { minimumFractionDigits: 0 });
    return formattedNPV;
  }