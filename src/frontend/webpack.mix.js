const mix = require("laravel-mix");

mix
  .js("src/js/app.js", "js")
  .postCss("src/css/app.css", "css", [
    require("tailwindcss"),
    require("autoprefixer"),
  ])
  .options({ processCssUrls: false })
  .webpackConfig({
    module: {
      rules: [
        {
          test: /\.js$/,
          enforce: "pre",
          use: ["source-map-loader"],
        },
      ],
    },
    devServer: {
      open: true,
    },
  })
  .copyDirectory("src/html/", "dist")
  .copyDirectory("src/images", "dist/images")
  .copyDirectory("src/fonts", "dist/fonts")
  .setPublicPath("dist")
  .disableNotifications();
