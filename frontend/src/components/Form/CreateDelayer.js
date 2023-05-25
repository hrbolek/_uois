/**
 * Vytvari zpozdovac,
 * @param {*} delay 
 * @returns 
 */
export const CreateDelayer = (delay=300) => {
    //lokalni promenna
    let oldTimer = -1;
    let state = 0;

    //navratovou hodnotou je funkce umoznujici zpozdeni volani
    return (delayedFunc) => {
        /*
        //https://stackoverflow.com/questions/26150232/resolve-javascript-promise-outside-the-promise-constructor-scope
        implement as function returning a Promise:

        const main = () => {
            let resolver = null
            const result = new Promise((resolve, reject) => {resolver = resolve})
            resolver(25)
            return result
        }

        main().then(data=>{console.log('a', data)})
        */
        //zruseni stareho timeru
        if (state !== 0) {
            clearTimeout(oldTimer)
            oldTimer = -1;
            state = 0;
        }

        //zabaleni funkce, pri volani je poznamenano, ze byl volan
        const encapsulatedFunc = () => {
            oldTimer = -1;
            state = 0;
            return delayedFunc(); // obvykle delayedFunc() vraci Promise, takze lze pouzit .then, .catch a .finally
        }

        //ocekavame zpozdene volani funkce
        state = 1;

        //definice noveho timeru
        oldTimer = setTimeout(encapsulatedFunc, delay);
    }
}