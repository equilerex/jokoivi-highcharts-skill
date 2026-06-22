---
tags: ["grid-pro"]
---

# Cell renderers

**Note:** Cell renderers are only available in Grid Pro. Grid Lite users can as an alternative use `formatter` and `format` to control [how data is rendered inside cells](./grid/cells/formatting).

Highcharts Grid Pro supports different cell renderers to provide interactive data presentation inside table cells. You can do this by setting the `columns[].cells.renderer` property for each column. This lets you control how each cell is displayed and interacted with, by e.g. turning a static value into an editable input field or a dropdown selector.

Cell renderers are also available in [edit mode](./grid/editing/index) by setting `columns[].cells.editMode.renderer`. This allows you to e.g. show plain text by default and present a checkbox or input field when a cell becomes editable.

## Default renderer

Unless specified the default renderer is `text`, and `textInput` in `editMode`. This can be plain text, and HTML markup is also supported. If needed the text/markup can be formatted using `formatter` or `format`, and Grid Pro users can also use the built-in renderers as described below.

## Input renderers

Using specific input types is preferable to relying on complex validation logic for plain text inputs because it leverages built-in browser behavior to enforce correct data formats. This reduces the need for custom code, minimizes validation errors, and improves performance. If more specific validation is needed, for e.g. string validation, please [refer to `validationRules`](./grid/editing/validation).

From a user experience perspective, typed inputs provide clearer intent, better accessibility, and context-appropriate interfaces.

The renderer API option can be set for both view and `editMode`. If not specified, the renderer for `editMode` is determined by `dataType`. When not in editMode it defaults to `text`.

Check out the todo app demo for how to implement renderers and read more below.

| renderer                                                                                                                                   | Description                                       | dataType        |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- | --------------- |
| `textInput`             | Text input that supports text/number and HTML     | string / number |
| `numberInput`       | Number input element                              | number          |
| `dateInput`             | Date input with datepicker                        | datetime        |
| `dateTimeInput` | Date and time input with date/time picker         | datetime        |
| `timeInput`             | Time input with time picker                       | datetime        |
| `checkbox`                | Checkbox input element                            | boolean         |
| `select`                      | Select element. Note that `options` are required. | string          |

You can further customize input renderers by using the `attributes` option. This allows you to pass additional HTML attributes to the underlying input element, such as `min`, `max`, `step`, `placeholder`, or any other valid attribute.
This is especially useful for number and date inputs, where you may want to restrict the allowed range or provide hints to users. For example:

```js
renderer: {
    type: 'numberInput',
    attributes: {
        min: 0,
        max: 100,
        step: 1
    }
}
```

### Text

Renders an editable text field for the value in editMode, and plain text/HTML when not in editMode. No specific configuration is needed since this is the default:

```js
columns: [{
    id: 'whatever', // column id
    cells: {
        editMode: {
            enabled: true
        }
    }
}]
```

### Date

Always renders a native date input. In `editMode` due to `dataType: 'datetime'`and is explicitly defined using `renderer` when not:

```js
columns: [{
    id: 'date', // column id
    dataType: 'datetime',
    cells: {
        renderer: {
            type: 'dateInput'
        }
    }
}]
```

### Checkbox

Renders a checkbox input element in `editMode` and uses `format` to display icons when not:

```js
columns: [{
    id: 'done', // column id
    cells: {
        dataType: 'boolean',
        format: '{#if value}✓{else}✗{/if}',
        editMode: {
            enabled: true
            renderer: {
                type: 'checkbox'
            }
        }
    }
}]
```

### Select

Renders a select element for predefined options in `editMode`. When not in `editMode` plain text is rendered:

```js
columns: [{
    id: 'country', // column id
    dataType: 'string',
    cells: {
        editMode: {
            renderer: {
                type: 'select',
                options: [
                    { value: 'NO', label: 'Norway' },
                    { value: 'NL', label: 'Netherlands' },
                    { value: 'PL', label: 'Poland' },
                    { value: 'EC', label: 'Ecuador' }
                ]
            }
        }
    }
}]
```

### Number

Renders an editable number field for the value in editMode, and plain text when not in editMode.

```js
columns: [{
    id: 'age', // column id
    dataType: 'number',
    cells: {
        renderer: {
            type: 'numberInput',
            attributes: { // optional properties
                min: 0,
                max: 100,
                step: 1
            }
        }
    }
}]
```

### Mixed

Renders a select element for predefined options when not in `editMode`. When in `editMode` a text input is used. `dataType: 'number'` is set to make sure number and not string is written to `DataTable` on updates, and `validationRules` is also applied to provide user feedback:

```js
columns: [{
    id: 'size', // column id
    dataType: 'number',
    cells: {
        renderer: {
            type: 'select',
            options: [
                { value: 1, label: 1 },
                { value: 2, label: 2 },
                { value: 3, label: 3 }
            ]
        },
        editMode: {
            renderer: {
                type: 'textInput'
            },
            validationRules: ['notEmpty', 'number']
        }
    }
}]
```

## Related articles

- [Validation](./grid/editing/validation)
- [Custom renderers](./grid/editing/custom-renderers)
