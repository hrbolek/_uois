module.exports = {
    presets: [
        ["@babel/preset-react",
            {
                targets: {
                    node: "current",
                },
            },
        ],
    ],
    plugins: [["babel-plugin-react-require"]]
};