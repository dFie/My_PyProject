import React from 'react';

const inject = obj => Comp => props => <Comp {...obj} {...props} />;

// let url = '?id=5&page=1&size=20&id=&age-20&name=abc&name=??=&??=1';

// function parse_qs(qs, re=/(\w+)=([^&]+)/) {
//     let obj = {};
//     if (qs.startsWith('?')) 
//         qs = qs.substr(1)
//     console.log(qs);
//     qs.split('&').forEach(element => {
//         let match = re.exec(element);
//         console.log(match)
//         if (match) obj[match[1]] = match[2];
//     });
//     return obj;
// }

// console.log(parse_qs(url))

const parse_qs = (qs, re=/(\w+)=([^&]+)/) => {
    let obj = {};
    if (qs.startsWith('?')) 
        qs = qs.substr(1);
    qs.split('&').forEach(
        element => {
            let match = re.exec(element);
            if (match) 
                obj[match[1]] = match[2];
        }
    );
    return obj;
}

export {inject, parse_qs};