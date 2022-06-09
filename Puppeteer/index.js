const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });
  const page = await browser.newPage();
  await page.goto(
    "https://www.jobstreet.com.ph/en/job-search/game-designer-jobs/",
    {
      waitUntil: "networkidle2",
    }
  );
  await page.setViewport({ width: 1420, height: 1080 });

  await browser.close();
})();
