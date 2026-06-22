const ts = require('typescript');
const fs = require('fs');
const path = require('path');

const skillDir = path.resolve(__dirname, '..');
const targetFile = path.join(skillDir, 'references', 'repo-copy', 'types-schemas', 'highcharts.d.ts');
const outputFile = path.join(skillDir, 'highcharts_api_map.json');

const program = ts.createProgram([targetFile], {});
const sourceFile = program.getSourceFile(targetFile);

const apiMap = {};

function visit(node) {
    if (ts.isInterfaceDeclaration(node) || ts.isClassDeclaration(node)) {
        const interfaceName = node.name ? node.name.text : 'Anonymous';
        if (interfaceName !== 'Anonymous') {
            apiMap[interfaceName] = { type: 'object', properties: {} };
            
            node.members.forEach(member => {
                if ((ts.isPropertySignature(member) || ts.isPropertyDeclaration(member)) && member.name) {
                    const propName = member.name.getText(sourceFile);
                    
                    const tags = ts.getJSDocTags(member);
                    const isDeprecated = tags.some(tag => tag.tagName.text === 'deprecated');
                    
                    // PRUNE DEPRECATED PROPERTIES entirely to prevent hallucination
                    if (!isDeprecated) {
                        apiMap[interfaceName].properties[propName] = {
                            optional: !!member.questionToken,
                            typeString: member.type ? member.type.getText(sourceFile) : 'any'
                        };
                    }
                }
            });
            
            // Prune interfaces that end up empty after removing deprecated props
            if (Object.keys(apiMap[interfaceName].properties).length === 0) {
                delete apiMap[interfaceName];
            }
        }
    }
    ts.forEachChild(node, visit);
}

if (sourceFile) {
    console.log("Parsing Highcharts TS definition...");
    ts.forEachChild(sourceFile, visit);
    fs.writeFileSync(outputFile, JSON.stringify(apiMap, null, 2));
    console.log(`Saved API map with ${Object.keys(apiMap).length} interfaces to ${outputFile}`);
} else {
    console.error(`Could not load ${targetFile}`);
}
