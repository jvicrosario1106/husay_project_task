const express = require("express");
const axios = require("axios");
const cors = require("cors");
const path = require("path");
const { convertArrayToCSV } = require("convert-array-to-csv");
const nodemailer = require("nodemailer");
const app = express();
const { Storage } = require("@google-cloud/storage");
const createCsvWriter = require("csv-writer").createObjectCsvWriter;
const fs = require("fs");

app.use(cors({ origin: true }));

const storage = new Storage({
  keyFilename: path.join(__dirname, "quick-hub-352911-1662e872c5a3.json"),
  projectId: "quick-hub-352911",
});

// Node Mailer
let transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: "dataanalytics369@gmail.com",
    pass: "dskotjtranfbceao",
  },
});

// API KEY For SerpAPI
const API_KEY =
  "407551c317011332165e248285b11b04620a1be883c5ce4b961b10378f123511";

app.get("/job-api/:page", (req, res) => {
  const listOfJobs = [
    // "graphic+designer", //
    // "illustrator", //
    "motion+graphics+artist", //
    // "producer", //
    // "artist", //
    // "creative+director", //
    // "game+designer", //
    // "multimedia+artist", //
    // "musician", //
    // "singer", //
    // "sound+engineer", // No Job List in API
  ];

  const { page } = req.params;

  // Looping Job List to Array
  listOfJobs.forEach((job) => {
    const datas = [];

    try {
      axios
        .get(
          `https://serpapi.com/search.json?engine=google_jobs&q=${job}+philippines&hl=en&api_key=${API_KEY}&start=${page}`
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

          // Insert To Company Type Array
          company_type.length > 0 &&
            company_type[0].options.map((ct) =>
              companyType.push({ companyType: ct.text })
            );

          // Employer Type
          let employerType = [];
          const employer = data.data.chips.filter(
            (chip) => chip.type === "Employer"
          );

          // Insert To Employer Array
          employer.length > 0 &&
            employer[0].options.map((ct) =>
              employerType.push({ employerType: ct.text })
            );

          // Array to CSV
          // const csvData = convertArrayToCSV(datas);
          // const ctData = convertArrayToCSV(companyType);
          // const etData = convertArrayToCSV(employerType);

          const csvWriter = createCsvWriter({
            path: `${job}.csv`,
            header: [
              { id: "title", title: "TITLE" },
              { id: "company", title: "COMPANY" },
              { id: "location", title: "LOCATION" },
              { id: "via", title: "VIA" },
              { id: "description", title: "DESCRIPTION" },
              { id: "extension", title: "EXTENSION" },
              { id: "scheduleType", title: "SCHEDULE" },
            ],
          });

          csvWriter
            .writeRecords(datas) // returns a promise
            .then(() => {
              console.log("...Done");
            });

          storage
            .bucket("jobs_csv_dataset")
            .upload(`./${job}.csv`, {
              destination: `jobs_dataset/${job}.csv.`,
            })
            .then(() => {
              fs.unlink(`${job}.csv`, function (err) {
                if (err) throw err;
                // if no error, file has been deleted successfully
                console.log("File deleted!");
              });
            });

          // Cloud Storage Config

          // Nodemailer Options
          // var mailOptions = {
          //   from: "dataanalytics369@gmail.com",
          //   to: "juliusrosario.senti@gmail.com",
          //   subject: "Job-API",
          //   text: "Job-API",
          //   html: "<b>Job-API</b>",
          //   attachments: [
          //     {
          //       filename: `${job}.csv`,
          //       content: csvData, // attaching csv in the content
          //     },
          //     {
          //       filename: `${job}-CT.csv`,
          //       content: ctData, // attaching csv in the content
          //     },
          //     {
          //       filename: `${job}-ET.csv`,
          //       content: etData, // attaching csv in the content
          //     },
          //   ],
          // };

          // // Sending Email ( CSV File Attachments )
          // transporter.sendMail(mailOptions, function (err, info) {
          //   if (err) {
          //     console.log("Err,", err);
          //   } else {
          //     console.log("Successfull");
          //   }
          // });
        })
        .catch((err) => console.log(err));
    } catch (err) {
      console.error("Error: ", err);
    }
  });
});

// Listen to Server
app.listen(3000, () => {
  console.log("Listing to port 3000");
});

// Exporting Server
module.exports = {
  app,
};
