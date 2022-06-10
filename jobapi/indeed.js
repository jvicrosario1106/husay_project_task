const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });
  const page = await browser.newPage();
  //   await page.setUserAgent(
  //     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
  //   );
  await page.setViewport({ width: 1520, height: 780 });
  await page.goto("https://ph.indeed.com/");

  await page.type("#text-input-what", "graphic designer");
  await page.waitForTimeout(3000);
  await page.click(".yosegi-InlineWhatWhere-primaryButton");
  await page.waitForTimeout(3000);
  const jobTitleLink = await page.$$(".jcs-JobTitle");

  for (let i = 0; i < jobTitleLink.length; i++) {
    await page.waitForTimeout(1000);
    await jobTitleLink[i].click();

    // const f = await page.$("#vjs-container-iframe");
    // const m = await f.contentFrame();
    // await page.waitForTimeout(1500);
  }
  const text = await page.evaluate(() => {
    let companies = [];
    const companyName = document.querySelectorAll(".companyName");
    companyName.forEach((company) => {
      companies.push(company.innerText);
    });
    return companies;
  });

  console.log(text);
})();
