import { DeleteButton } from "@uoisfrontend/shared";
import { CheckLg, TrashFill } from "react-bootstrap-icons";
import { action } from '@storybook/addon-actions';
import { withRouter } from 'storybook-addon-react-router-v6';

const meta = {
    //👇 component which is all about
    component: DeleteButton,
    //👇 Tree position where those stories will be placed
    title: "Shared/DeleteButton",
    //👇 Needed for componets using react-router library
    decorators: [withRouter],

    //👇 Args for the component's play
    argTypes: {
        onClick: {action: "clicked"},
        icon: {
            options: ["TrashFill", "CheckLg" ],
            mapping: {
                TrashFill: <TrashFill />,
                CheckLg: <CheckLg />,
            },
            control: { type: 'radio' }
        },
    },
    //👇 Enables auto-generated documentation for the component story
    tags: ['autodocs'],
};

export default meta;

/*
 *👇 Render functions are a framework specific feature to allow you control on how the component renders.
 * See https://storybook.js.org/docs/react/api/csf
 * to learn how to use render functions.
 */
export const Primary = {
    name: "Primary",
    //👇 Initial value for args
    args: {
        // icon: <TrashFill />,
        icon: "TrashFill",
        onClick: action("clicked")
    },
    parameters: {
        backgrounds: {
          values: [
            { name: 'red', value: '#f00' },
            { name: 'green', value: '#0f0' },
          ],
        },

        reactRouter: {
            routePath: '/users/:userId',
            routeParams: { userId: '42' },
            routeHandle: "Profile",
            searchParams: { tab: 'activityLog' },
            routeState: { fromPage: 'homePage' },
        }
      },
    
    // actions: { argTypesRegex: '^on[A-Z].*' },

    //👇 how the component will be rendered
    render: (args) => <DeleteButton onClick={args.onClick}>{args.icon}</DeleteButton>,
};