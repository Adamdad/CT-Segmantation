import matplotlib.pyplot as pltimport numpy as npimport torchvisionimport torchfrom utils.dataset import *from models.Unet import UNetfrom tqdm import  tqdmimport argparsefrom torch.utils.data import DataLoaderfrom models.ResUnet import ResUNetfrom PIL import Image# functions to show an imagedef imshow(img, save_name ='true.png' ):    img = img / 2 + 0.5     # unnormalize    npimg = img.numpy()    plt.figure(figsize=(10,5))    plt.imshow(np.transpose(npimg, (1, 2, 0)))    plt.savefig(save_name)def imshow_pred(img, save_name ='result.png'):    npimg = img.numpy() * 255    plt.figure(figsize=(10, 5))    plt.imshow(np.transpose(npimg, (1, 2, 0)))    plt.savefig(save_name)parser = argparse.ArgumentParser(description='Image Classification.')parser.add_argument('--image-dir', type=str, default='../data/dataset_5_10/data/4_4_data_crop')parser.add_argument('--mask-dir', type=str, default='../data/dataset_5_10/data/med_seg_lungmask')parser.add_argument('--newmask-dir', type=str, default='../data/dataset_5_10/data/med_seg_lungmask_gen')parser.add_argument('--test-COVID', type=str,                        default='../data/dataset_5_10/test_COVID.txt')parser.add_argument('--test-NonCOVID', type=str,                    default='../data/dataset_5_10/test_NonCOVID.txt')parser.add_argument('--checkpoint', type=str, default='./checkpoint/ResUnet/best.pth.tar')args = parser.parse_args()test_transform = transforms.Compose([        transforms.Resize((320, 400)),        transforms.ToTensor(),        transforms.Normalize(mean=[0.5, 0.5, 0.5],                  std=[0.5, 0.5, 0.5])    ])if os.path.exists(args.newmask_dir)==False:    os.makedirs(args.newmask_dir)images = ['CT_COVID/{}'.format(name) for name in np.loadtxt(args.test_COVID, dtype=str)]+ \                      ['CT_NonCOVID/{}'.format(name) for name in np.loadtxt(args.test_NonCOVID, dtype=str)]device = torch.device("cuda" if torch.cuda.is_available() else "cpu")model = ResUNet().to(device)checkpoint = torch.load(args.checkpoint, map_location="cpu")state_dict = checkpoint['state_dict']msg = model.load_state_dict(state_dict)print("Model Loaded")for name in images:    print(name)    image_path = os.path.join(args.image_dir,name)    img = Image.open(image_path).convert('RGB')    img_tensor = test_transform(img).unsqueeze(0).to(device)    output = model(img_tensor)    _, preds = torch.max(output, 1)    preds = torch.cat([preds, preds, preds], dim=0)    preds = preds.data.cpu().numpy() * 255    preds = np.transpose(preds, (1, 2, 0)).astype(np.uint8)    preds = Image.fromarray(preds)    preds.save(os.path.join(args.newmask_dir,name))# for index, batch in enumerate(tqdm(test_loader)):#     images, labels = batch['img'], batch['label']#     # show images#     imshow(torchvision.utils.make_grid(images,nrow=4),save_name='visual/{}image'.format(index))#     # show label#     labels_image = torch.cat([labels.unsqueeze(1),labels.unsqueeze(1),labels.unsqueeze(1)],dim=1)#     imshow_pred(torchvision.utils.make_grid(labels_image,nrow=4),save_name='visual/{}label'.format(index))#     # show pred#     output = model(images.to(device))#     _, preds = torch.max(output, 1)#     preds = torch.cat([preds.unsqueeze(1),preds.unsqueeze(1),preds.unsqueeze(1)],dim=1)#     imshow_pred(torchvision.utils.make_grid(preds.cpu(),nrow=4),save_name='visual/{}pred'.format(index))