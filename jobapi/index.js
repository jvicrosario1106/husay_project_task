const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });
  const page = await browser.newPage();
  await page.setUserAgent(
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
  );
  await page.goto(
    "https://www.jobstreet.com.ph/en/job-search/game-designer-jobs/",
    {
      waitUntil: "networkidle2",
    }
  );
  await page.setViewport({ width: 1420, height: 1600 });

  const getArticles = await page.evaluate(() => {
    const articles = document.querySelectorAll(
      ".sx2jih0.zcydq89e.zcydq88e.zcydq872.zcydq87e h1"
    );

    let listArticle = [];
    articles.forEach((article) => {
      listArticle.push(article.innerText);
    });

    return listArticle;
  });

  const jobTitleLink = page.$$(".sx2jih0.zcydq89e.zcydq88e.zcydq872.zcydq87e");

  for (let i = 0; i < jobTitleLink.length; i++) {
    jobTitleLink[i].click();

    while (
      page.url() !==
      "https://www.jobstreet.com.ph/en/job-search/game-designer-jobs/"
    ) {
      page.waitForTimeout(3000);
      page.goBack({ waitUntil: "networkidle2" });
      page.waitForTimeout(3000);
    }
  }
})();
