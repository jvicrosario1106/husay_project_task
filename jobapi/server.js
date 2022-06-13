const express = require("express");
const axios = require("axios");
const cors = require("cors");
const { convertArrayToCSV } = require("convert-array-to-csv");
const nodemailer = require("nodemailer");
const app = express();

app.use(cors({ origin: true }));

// Node Mailer
let transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "dataanalytics369@gmail.com",
    pass: "dskotjtranfbceao",
  },
});

const API_KEY =
  "c06cc87167ff82c14347678ee97e37dcadfbcef75692e41e8cc1c71f29d62a01";

app.get("/job-api", (req, res) => {
  const listOfJobs = [
    "graphic+designer", //
    "illustrator", //
    "motion+graphics+artist", //
    "producer", //
    "artist", //
    "creative+director", //
    "game+designer", //
    "multimedia+artist", //
    "musician", //
    "singer", //
    // "sound+engineer",
  ];

  listOfJobs.forEach((job) => {
    const datas = [];

    try {
      axios
        .get(
          `https://serpapi.com/search.json?engine=google_jobs&q=${job}+philippines&hl=en&api_key=${API_KEY}`
        )
        .then((data) => {
          data.data.jobs_results.map((results) => {
            datas.push({
              title: results.title,
              company: results.company_name,
              location: results.location,
              via: results.via,
              description: results.description,
              extension: results.extensions[1],
              scheduleType:
                results.detected_extensions.schedule_type &&
                results.detected_extensions.schedule_type,
            });
          });

          // Company Type
          let companyType = [];
          const company_type = data.data.chips.filter(
            (chip) => chip.type === "Company type"
          );

          company_type.length > 0 &&
            company_type[0].options.map((ct) =>
              companyType.push({ companyType: ct.text })
            );

          // Employer Type
          let employerType = [];
          const employer = data.data.chips.filter(
            (chip) => chip.type === "Employer"
          );

          employer.length > 0 &&
            employer[0].options.map((ct) =>
              employerType.push({ employerType: ct.text })
            );

          // Array to CSV
          const csvData = convertArrayToCSV(datas);
          const ctData = convertArrayToCSV(companyType);
          const etData = convertArrayToCSV(employerType);

          //Nodemailer Options
          var mailOptions = {
            from: "dataanalytics369@gmail.com",
            to: "juliusrosario.senti@gmail.com",
            subject: "Job-API",
            text: "Job-API",
            html: "<b>Job-API</b>",
            attachments: [
              {
                filename: `${job}.csv`,
                content: csvData, // attaching csv in the content
              },
              {
                filename: `${job}-CT.csv`,
                content: ctData, // attaching csv in the content
              },
              {
                filename: `${job}-ET.csv`,
                content: etData, // attaching csv in the content
              },
            ],
          };

          transporter.sendMail(mailOptions, function (err, info) {
            if (err) {
              console.log("Err,", err);
            } else {
              console.log("Successfull");
            }
          });
        })
        .catch((err) => console.log(err));
    } catch (err) {
      console.error("Error: ", err);
    }
  });
});

app.listen(3000, () => {
  console.log("Listing to port 3000");
});
